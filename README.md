 # Contract Information Extraction from Scanned PDF using OpenAI and LangChain

This project extracts essential information from a Persian-language contract provided as a scanned PDF file. It uses OpenAI's GPT model and LangChain to parse images of the contract and extract key details such as the subject of the contract, the client's name, and the contract's start date.

## Overview

The project processes the provided PDF by converting its pages into images and then passing them through OpenAI's GPT-4 model to extract contract details. The extracted information is structured into a predefined format, which includes:

- **Subject of the Contract (موضوع قرارداد)**
- **Client's Name (کارفرما)**
- **Contract Start Date (تاریخ شروع قرارداد)**

The extracted details are then printed for review.

## Installation

To run this project, you will need to have the following dependencies installed:

1. **OpenAI Python Client**: Required to interact with the OpenAI API.
2. **LangChain**: Required to handle the chain of processing steps for the contract extraction.
3. **pdf2image**: Required to convert PDF pages into images.
4. **Pillow (PIL)**: Required for image manipulation.
5. **Pydantic**: For data validation and creating structured output.

### Install the required libraries

You can install all necessary libraries using the following command:

```bash
pip install openai langchain pdf2image pillow pydantic requests
