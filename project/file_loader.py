def load_data(valid_class_file, invalid_class_file, fold_validation=5):
    with open(valid_class_file) as f:
        valid_lines = f.readlines()

    with open(invalid_class_file) as f:
        invalid_lines = f.readlines()

    # Setting the size to fit into the fold validation
    smallest_length = len(valid_lines) if len(valid_lines) < len(invalid_lines) else len(invalid_lines)
    data_size = smallest_length / fold_validation
    data_size *= fold_validation
    valid_lines = valid_lines[:data_size]
    invalid_lines = invalid_lines[:data_size]

    # Formatting strings to list
    valid_lines = [map(int, list(x.strip())) for x in valid_lines]
    invalid_lines = [map(int, list(x.strip())) for x in invalid_lines]

    # Returning the list
    return valid_lines, invalid_lines, len(valid_lines[0])


def Load_File_Data(file_name, fold_validation=5):
    current_class = -1

    class_data = []
    new_data = []
    feature_threshold = []
    num_features = 0

    with open(file_name) as f:
        lines = f.readlines()
        lines = [x.strip() for x in lines]

        for line in lines:
            elements = line.split(',')
            new_class = elements.pop(0)

            if new_class != current_class:
                current_class = new_class
                class_data.append([])

            new_data = [float(i) for i in elements]

            class_data[-1].append(new_data)

            for i, element in enumerate(new_data):
                if len(feature_threshold) < len(new_data):
                    feature_threshold.append(0)

                feature_threshold[i] += element
            if num_features < len(feature_threshold):
                num_features = len(feature_threshold)

    for n in range(len(feature_threshold)):
        feature_threshold[n] /= float(len(lines))

    # Get smallest list so we can get all classes same length
    smallest_length = float('inf')
    for single_class in class_data:
        if len(single_class) < smallest_length:
            smallest_length = len(single_class)

    size = smallest_length / fold_validation
    size *= fold_validation

    # Modify list so it fits fold validation
    for x in range(len(class_data)):
        class_data[x] = class_data[x][:size]

    # Convert our data to binary by thresholding each class
    for data_class in class_data:
        for data in data_class:
            for i in range(0, len(data)):
                if data[i] > feature_threshold[i]:
                    data[i] = 1
                else:
                    data[i] = 0
    return class_data, num_features
