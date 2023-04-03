### Executive Summary

The goal of this notebook is to use a combination of clinical, genetic, and transcriptomic data as inputs to ML models in order to better understand 1) predictive factors of a patient's overall survival (supervised ML) in Non-small-cell lung cancer (NSCLC)  and 2) identifying underlying patterns and/or attributes that are either shared or unique to each NSCLC subtype included here, LUAD and LUSC. 

### Highlights of Procedure

To achieve goal 1, I mainly tested a RandomForestClassifier (RFC) wrapped in a GridSearchCV and Sklearn Pipeline. RFC is not sensitive to scaling of features, and can accomodate lots of different kinds of features over different ranges. While an RFC can be prone to overfitting, setting some key parameters like `max_depth` and `max_features` can help to avoid overfitting.

I compared the following strategies: 1) manual feature subsetting, 2) Principal Componenet Analysis (PCA), a linear dimensionality reduction technique, and 3) Uniform Manifold Approximation and Projection (UMAP), a non-linear dimension reduction algorithm. These strategies were applied to: 1) clinical data only; 2) genetic data only; 3) transcriptomic data only; 4) a combination of genetic+transcriptomic data.     

Some next steps for this analysis include: 1) Testing more models than an RFC like XGB (I did start testing out the XGB but ran into some bugs where (I think) the input data matrix was so sparse, XGB could not load the trained model properly for the test set because it would drop some features (similar to [this bug](https://github.com/dmlc/xgboost/issues/1238)); 2) Doing some additional feature selection with more in-depth differential gene expression analysis and minimum Redundancy - Maximum Relevance feature selection; 3) more in-depth correlation testing to see if I could drop some highly correlated features that may be more biologically meaningful than the PCA/UMAP transformations. 

### Highlights of Findings
-Clinical features could predict OS_STATUS with ~75% accuracy (and predicted LUSC v. LUAD subtypes with 100% accuracy, the subtype model was significantly overfit)
-Genetic mutations alone could not predict OS_STATUS much better than chance, and performance degraded when PCA was applied. My interpretation of these findings is that many genetic mutations are contributing to OS_STATUS differences but each is doing so just a little bit. Polygenic Risk Score analysis would be super interesting here! 
