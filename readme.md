# **Image segmentation of fly embryos**

The following is information describing the content of the project and how to run the code. 

## **How to run the files?**

1. Download this Github folder.
1. Download the zip containing the data from this Google Drive link: (https://drive.google.com/file/d/12s9NyoeqFkfLo755-Qdh0RGFtWLMjzCN/view?usp=sharing)
1. Put the **Dataset** folder contained in the zip file inside the Github folder downloaded in **step 1**.
1. Then run the below python files that you would like to analyze.

1. **(Optional) If you don't have an updated version of skimage** you might not be able to run **cell_segmentation_Abdolhosseini_et_al.py**. If you would like to update skimage, here is a list of instructions to do so, since you might encounter some problems by trying to update skimage directly. The following work around is to uninstall then reinstall skimage. 
    ```
    conda uninstall scikit-image
    
    conda install -c conda-forge scikit-image
    
    pip install -r requirements.txt --no-index --find-links file:///tmp/packages
    ```

## **Python files:**


* **cell_counting.py**: Cell counting module, you can choose the file you want to execute at the beginning of the script. The script will plot the different steps of the cell counting. 
* **final_segmentation_method.py**: Our final segmentation method and avg cell size calculation. It has the same structure as cell_counting.py, plots will show the different steps of segmentation and cell size estimation.  
* **cell_segmentation_Abdolhosseini_et_al.py**: Similar to final_segmentation_method.py but with Abdolhosseini et al's method. 
* **stats<span></span>.py**: Statistics on the cell count and cell size per stage. Executing it will give the distribution of these features accross all images, as well as aggregates per stage.
* **PCA<span></span>.py:** This will run the different feature exctraction scripts listed below, including the PCA/ICA and the SVM classifier and its results. Execution takes takes ~15 min for the whole process. 
* **imageAlignment<span></span>.py**: Align images according to the standard shape.
* **headClassifier<span></span>.py**: Classifies the images based on the manual labelling of the presence of a bright head in the left side of the gene expression. It recquires to first run the preprocessing in **PCA<span></span>.py** .

## **Other files and folders:**

* **report.pdf**: Contains the report
* **embryo_evolution.mov**: Contains a clip of the embryo’s evolution, our dataset corresponds to the first 30 seconds. If you cannot read the file, you can do so with VLC media player. 
* **Dataset Folder**: Contains the dataset described in the report. 
* **Other Folders (Embryos, GeneExpression, Rectangles etc...)**: These are empty folders for the PCA<span></span>.py script. After you run it, they will contain the processed data necessary for the PCA.




