# ChangeLog

## [v1.0.0-Eagle] - 2026-02-21

## Eagle Refactoring & Windows Support

- Completely restructured and deeply renamed the `Sparrow` codebase to `Eagle`.
- Removed WSL-incompatible native desktop tracking scripts.
- Added `eagle_capture.py` and `build_capture_exe.bat` to support native PyInstaller executable builds on Windows to bypass headless WSL screen capture limitations.
- Preserved structured data extraction and instruction calling using ML/Vision LLMs.
- Acknowledged original KatanaML Sparrow repository as the foundation.

## [v0.4.4] - 2025-09-27

## New MLX backend

Improved Eagle backend with upgraded MLX libs, new Mistral 3.2 model and improved UI.


## [v0.4.3] - 2025-05-24

## Data Annotation Support

Enhanced document processing with bounding box annotations and visual coordinate extraction for precise field location tracking



## [v0.4.2] - 2025-05-08

## LLM instruction calling

Microservice approach for LLM request processing with instruction calling



## [v.0.4.1] - 2025-04-11

## Eagle UI Dashboard

Added dashboard to Eagle UI to visualize system performance


## [v.0.4.0] - 2025-03-29

## Free tier and new vision backend models

Eagle is updated with new free tier functionality for https://eagle.katanaml.io/. New vision backend models are integrated, such as Mistral Small 3.1 and Qwen 2.5 72B


## [v0.3.0] - 2025-03-09

## Eagle Agent

Added Eagle Agent functionality to orchestrate complex document processing tasks. This new component allows you to combine multiple data extraction operations into a single workflow with visual monitoring and tracking through Prefect integration. Users can now process documents through an intuitive API that handles classification, extraction, and validation in one seamless pipeline.


## [v0.2.4] - 2025-01-23

## Image Cropping and UI Shell updates

Implemented image cropping, this is useful for form pages, to reduce overall image size. Add various UI improvements to Eagle UI Shell, enabled better logging

This release brings Eagle deployment on local Mac Mini M4 Pro 64GB machine - https://eagle.katanaml.io


## [v0.2.3] - 2024-12-16

## Table processing

Added support auto detect tables and send cropped table images for inference


## [v0.2.2] - 2024-11-24

## Multi-page PDF document support

Added support for multi-page PDF document through CMD and API

## [v0.2.1] - 2024-11-08

## Dependencies cleanup

Removed dependencies to LlamaIndex, Haystack, Unstructured and other libraries, as main Eagle focus is on Eagle Parse

## [v0.2.0] - 2024-09-04

## Eagle Parse with Vision LLM support

This release starts new phase in Eagle development - Vision LLM support for document data processing.

1. Eagle Parse library supports Vision LLM
2. Eagle Parse provides factory class implementation to run inference locally or on cloud GPU
3. Eagle supports JSON as input query
4. JSON query validation and LLM response JSON validation is performed

## [v0.1.8] - 2024-07-02

### New Features

- Eagle Parse integration

### What's Changed

- Eagle Parse is integrated into Instructor agent. README updated with example for Instructor agent

  

## [v0.1.7] - 2024-04-23

### New Features

- New Instructor agent

### What's Changed

- Added instructor agent for better JSON response generation



## [v0.1.6] - 2024-04-17

### New Features

- New agents with Unstructured

### What's Changed

- Added unstructured-light and unstructured agents for better data pre-processing




## [v0.1.5] - 2024-03-27

### New Features

- Virtual Environments support

### What's Changed

- Fixes in LlamaIndex agent to run with latest LlamaIndex versions
- LLM function calling agent




## [v0.1.4] - 2024-03-07

### New Features

- OCR + LLM support, new vprocessor agent

### What's Changed

- Improved FastAPI endpoints




## [v0.1.3] - 2024-02-11

### New Features

- Added Haystack agent for structured data

### What's Changed

- Changed plugins to agents

  

## [v0.1.2] - 2024-01-31

### New Features

- Added support for plugin architecture. This allows to use within Eagle various toolkits, such as LlamaIndex or Haystack

### What's Changed

- Significant code refactoring

  

## [v0.1.1] - 2024-01-19

### New Features

- Minor improvements related to data ingestion

### What's Changed

- Fixed bug to clean Vector DB, when new document is inserted
- Tested with Notus and Openhermes LLMs
- Tested with longer and more realistic documents
- Upgraded LlamaIndex and LangChain



## [v0.1.0] - 2024-01-12

### New Features

- Lemming LLM RAG

### What's Changed

- 
