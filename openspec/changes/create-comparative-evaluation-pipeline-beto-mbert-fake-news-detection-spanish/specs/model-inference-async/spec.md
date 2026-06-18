## ADDED Requirements

### Requirement: System can perform async inference using BETO model
The system SHALL be able to perform async inference using the BETO model for Spanish fake news detection.

#### Scenario: BETO model inference
- **WHEN** user requests BETO model inference
- **THEN** system performs async inference and returns prediction

### Requirement: System can perform async inference using mBERT model
The system SHALL be able to perform async inference using the mBERT model for Spanish fake news detection.

#### Scenario: mBERT model inference
- **WHEN** user requests mBERT model inference
- **THEN** system performs async inference and returns prediction

### Requirement: System can measure inference time
The system SHALL be able to measure and record the execution time of model inference.

#### Scenario: Inference timing
- **WHEN** model inference completes
- **THEN** system records and stores the execution time