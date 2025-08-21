import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )
    
    # Normalization, Adjusting better parameters
    # scaler = StandardScaler()
    # X_train = scaler.fit_transform(X_train)
    # X_test = scaler.transform(X_test)

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename: str) -> tuple[list, list]:
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    count: int = 0
    evidence: list = []
    month: dict = {"Jan": 0, "Feb": 1, "Mar": 2, "Apr": 3, "May": 4,
                   "June": 5, "Jul": 6, "Aug": 7, "Sep": 8, "Oct": 9,
                   "Nov": 10, "Dec": 11,
                   }
    visitortype: dict = {"Returning_Visitor": 1, "New_Visitor": 0, "Other": 0}
    weekend: dict = {"FALSE": 0, "TRUE": 1}
    labels: list = []

    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        # Skip 0 row
        next(reader)
        for line in reader:
            # print(line)
            evidence_row = [
                int(line[0]), float(line[1]), int(line[2]),
                float(line[3]), int(line[4]), float(line[5]),
                float(line[6]), float(line[7]), float(line[8]),
                float(line[9]), month[line[10]], int(line[11]),
                int(line[12]), int(line[13]), int(line[14]),
                visitortype[line[15]], weekend[line[16]],
            ]
            evidence.append(evidence_row)

            label = 1 if line[17] == "TRUE" else 0
            labels.append(label)

    return (evidence, labels)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    neigh = KNeighborsClassifier(n_neighbors=5, weights='distance')
    neigh.fit(evidence, labels)

    return neigh

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    sensitivity = float
    specificity = float
    
    tn, fp, fn, tp = confusion_matrix(labels, predictions).ravel()
    sensitivity = tp / (tp + fn)
    specificity = 1 - sensitivity
    
    return (sensitivity, specificity)

if __name__ == "__main__":
    main()
