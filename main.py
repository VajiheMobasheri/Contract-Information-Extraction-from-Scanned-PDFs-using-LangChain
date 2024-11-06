from openai import OpenAI
import os
import base64
from pydantic import BaseModel, Field
import requests
from pprint import pprint
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import httpx
from pdf2image import convert_from_path
from PIL import Image


my_api_key = os.environ["OPENAI_API_KEY"]


pdf_path = "./Your_pdf_file.pdf"
images = convert_from_path(pdf_path)

model = ChatOpenAI(model="gpt-4o")


class Item(BaseModel):
    found: bool = Field(
        description="Whether or not Item exists on this image. Always check for existing in many cases the Item is not exist. "
    )
    value: str = Field(description="Extracted value of Item.")
    position: str = Field(
        description="If you found Item in the image, please provide approximate position of Item in the image."
    )
    page_number: str = Field(description="Extracted the page number of the Item.")


class Output(BaseModel):
    subject: Item = Field(
        description="the main topic of the contract, keyword in Persian: 'موضوع قرارداد'"
    )
    client_name: Item = Field(
        description="the name of the client involved in this contract, keyword in Persian: 'کارفرما' "
    )
    contract_start_date: Item = Field(
        description="the date the contract was signed, keyword in Persian: 'تاریخ شروع قرارداد' "
    )


parser = JsonOutputParser(pydantic_object=Output)

initial_message = {
    "type": "text",
    "text": f"""\
You have been provided with an image containing a Persian-language contract. Your task is to extract essential information from this contract and present your findings in Persian. If any information cannot be extracted, do not make assumptions or fabricate data. Always becareful with numeric types They are very misleading; It is better to say not exist than fabricate it.
{parser.get_format_instructions()}
""",
}

response_dict = {
    "subject": {"found": None, "value": None, "position": None, "page_number": None},
    "client_name": {
        "found": None,
        "value": None,
        "position": None,
        "page_number": None,
    },
    "contract_start_date": {
        "found": None,
        "value": None,
        "position": None,
        "page_number": None,
    },
}

max_images = 5
final_response = ""

for i, image in enumerate(images):
    if i >= max_images:
        break

    else:
        image = image.resize(
            (int(1200 * (image.width / image.height)), 1200), Image.LANCZOS
        )
        image_path = f"page_{i + 1}.png"
        image.save(image_path, "PNG")
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        content = [
            initial_message,
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{encoded_string}"},
            },
        ]
        message = HumanMessage(content=content)
        chain = model | parser
        response = chain.invoke([message])

        if response:
            for key, item in response.items():
                if item["found"]:
                    response_dict[key] = item

        if all(item["found"] is not None for item in response_dict.values()):
            break


pprint(response_dict)
