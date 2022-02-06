# assignment_MLOps-Home
This repository will be used to store all relevant scripts for the assignment of MLOps@Home

## Directory structure
```
.
├── azure_folder                    // Contains the scripts used on AMLS
├── Cedric_Hermans_assignment.docx  // The Word document that was also uploaded on Leho
├── download_sequences.py           // The script used to download the training sequences
├── example_fastas                  // Example FASTA files, useful for testing.
├── FastAPI_and_Docker              // The folder containing everything for FastAPI app
│   ├── api
│   │   ├── app
│   │   │   ├── main.py             // Main script for app
│   │   │   └── model               // Helperfunctions for AI model
│   │   │       └── model.py
│   │   ├── best_model
│   │   │   └── gene-nn             // The best model selected from AMLS
│   │   └── requirements.dev.txt    // Requirements needed for the app
│   ├── docker-compose.yml          // Docker compose file
│   └── Dockerfile                  // Docker file
├── LICENSE                         // License information
├── neural-network-structure.svg    // SVG of the used NN structure
└── README.md                       // This file
```
## Links
* [video showcasing the API](https://howest.cloud.panopto.eu/Panopto/Pages/Viewer.aspx?id=7f16ce1c-5574-4eb5-8d2b-ae340111bd65)
* [deployment on Kubernetes cluster](https://localhost:32000/dashboard/c/local/explorer/apps.deployment/hermans-cedric-assignment/nrps-pks-predictor#pods)