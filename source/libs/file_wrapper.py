import joblib

class FileWrapper:
    def __init__(self, filename):
        self.filename = filename

    def create(self, data):
        try:
            with open(self.filename, 'wb') as file:
                joblib.dump(data, file)
            print("Data created successfully.")
        except Exception as e:
            print(f"Error creating data: {str(e)}")

    def read(self):
        try:
            with open(self.filename, 'rb') as file:
                data = joblib.load(file)
                return data
        except Exception as e:
            print(f"Error reading data: {str(e)}")
            return None

    def update(self, new_data):
        existing_data = self.read()
        if existing_data is not None:
            try:
                with open(self.filename, 'wb') as file:
                    merged_data = {**existing_data, **new_data}
                    joblib.dump(merged_data, file)
                print("Data updated successfully.")
            except Exception as e:
                print(f"Error updating data: {str(e)}")

    def delete(self):
        try:
            with open(self.filename, 'wb') as file:
                joblib.dump({}, file)
            print("Data deleted successfully.")
        except Exception as e:
            print(f"Error deleting data: {str(e)}")

# # Example usage:
# if __name__ == "__main__":
#     crud = FileCRUD("data.joblib")
#
#     # Create data
#     data_to_create = {'item1': 42, 'item2': 'example'}
#     crud.create(data_to_create)
#
#     # Read data
#     read_data = crud.read()
#     print("Read data:", read_data)
#
#     # Update data
#     data_to_update = {'item3': [1, 2, 3]}
#     crud.update(data_to_update)
#     updated_data = crud.read()
#     print("Updated data:", updated_data)
#
#     # Delete data
#     crud.delete()
#     deleted_data = crud.read()
#     print("Deleted data:", deleted_data)
