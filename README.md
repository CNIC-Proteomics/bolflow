# bolflow

# Workflow steps

## Data pre-processing
1. Combine the 2 matrixes: 0-6 -> take min 0-5;  4-11 -> take min 5-11
2. Add classification to the matrix of data

## Data processing

### Calculation
1. Calculate frequency per group of samples, per single batch, per cohort and global
2. Calculate frequency of QCs per single batch, per cohort and global
3. Calculate CV% in QCs per single batch, per cohort and global

### Filtering
4. Filtering 0: Discard duplicates
5. Filtering 1: keeping features that are present at least in the 75% of one group of samples (control and disease) in each cohort, and in at least the 10% in all group of samples per cohort.
6. Replacing Missing Values with KNN 
7. Filtering 2: keeping features that are present at least in the 80% of samples in at least one group of samples (e.g. for PESA Controls and Diseases)
8. Normalization (include different strategies i.e. LOESS/COMBAT)
9. Filtering 3: keeping features that present a CV% in QCs lower than 30% [make it optional]
10. LOG transformation of the value with addition of constant value


Scaling ?
Fold change calculation?

