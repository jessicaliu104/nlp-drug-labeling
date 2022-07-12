# Annotating adverse reactions in drug labeling using AI model
This repository contains the code for my 2022 NCTR summer student research project. 

### Background and Motivation
Adverse drug reactions (ADRs) are unintended, undesirable effects that a drug may have. They are public health concerns, as they can result in life threatening events, such as death. Drug labels are descriptions of the drugs. They are a primary source for ADR records. ADRs of a drug are outlined in three sections: Boxed Warning, Warnings and Precautions, and Adverse Reactions. Currently, there are no drug labeling knowledge bases/resources that contain well-maintained ADR annotations (see related works).

### Related Works
  - [SIDER](http://sideeffects.embl.de/) 

SIDER is a database that contains information on marketed medicines and their recorded ADRs. The information is mainly extracted from public documents and package inserts. However, SIDER uses MedDRA to manually code for adverse reactions, which can be a slow and tedious process. There is no available positional annotated data. This makes data preparation almost impossible because the annotation doesn't contain the start and end position.
Additionally, the current version (SIDER 4.1) was released on October 21, 2015. This is outdated and might not represent the most up-to-date and accurate information. 
  - [TAC 2017: Adverse Drug Reaction Extraction from Drug Labels](https://bionlp.nlm.nih.gov/tac2017adversereactions/)

The Text Analysis Conference (TAC) is a series of evaluation workshops. The purpose of the 2017 TAC track was to test different natural language processing (NLP) approaches for their information extraction performance on adverse reactions found in labels. Participants were provided with 101 labeling samples for training. The results indicated the median performance was around 0.70, with the best performance being 0.82.

### Datasets and Methods
The data used is from [TAC 2017: Adverse Drug Reaction Extraction from Drug Labels](https://bionlp.nlm.nih.gov/tac2017adversereactions/). One dataset used is the 101 released labeling samples from TAC2017. The other dataset, DPV-100, contained 100 annotated documents.
  - `data processing.py` contains the code for processing the 101 released labeling samples into the form that is used by the model. 

### Study Design
The language model used is RxBERT. The 101 released labeling samples were split into 239 sections. 190 sections were used as training data for the model and 49 sections were used as testing data. Next, the RxBERT NER model trained by the TAC2017 data was tested on the DPV-100 dataset. 


### Results
<img width="712" alt="Screen Shot 2022-07-11 at 9 28 41 PM" src="https://user-images.githubusercontent.com/106784802/178395443-ed906e92-2e65-4996-bf4b-a989ea16f1fb.png">
After around 100 epochs on the TAC2017 101 released samples, the evaluating performance saturated. The recall of the model is ~85%. Additionally, the model can find ~20% of terms that had not been annotated. 

<img width="538" alt="Screen Shot 2022-07-11 at 9 31 23 PM" src="https://user-images.githubusercontent.com/106784802/178395754-71ea6829-4f0b-4e6c-949a-2d79bc66afdf.png">
This is the final result on the testing data (49 sections) using the RxBERT NLP model after 200 epochs. The final result had a precision of 86.6%, recall of 86.3% and F1 of 86.45%. This is slightly better than the top performer of the 2017 TAC, which had a precision of 82.5%, recall of 82.4%, and F1 of 82.5%. 

