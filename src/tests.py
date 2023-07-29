import os
import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

tests_folder = os.path.dirname(os.path.abspath(__file__))
test_data_path = os.path.join(tests_folder, 'tests_case', 'test_data.csv')

def test_upload_file(client):
    # Проверяем успешную загрузку файла
    filename = 'test_file.csv'
    data = {'file': (open(test_data_path, 'rb'), filename)}
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert b"File uploaded successfully" in response.data

    # Проверяем, что файл действительно загружен
    uploaded_files = os.listdir('uploads')
    assert filename in uploaded_files


def test_get_files(client):
    # Проверяем получение списка файлов
    response = client.get('/files')
    assert response.status_code == 200
    assert b"test_file.csv" in response.data


def test_get_data(client):
    # Проверяем получение данных из файла
    response = client.get('/data?filename=test_file.csv')
    assert response.status_code == 200
    assert b"First Name" in response.data

    # Проверяем фильтрацию данных по значению в столбце
    response = client.get('/data?filename=test_file.csv&column=Age&value=25')
    assert response.status_code == 200
    assert b"John" in response.data
    assert b"Lisa" not in response.data

    # Проверяем сортировку данных по столбцу
    response = client.get('/data?filename=test_file.csv&sort_by=Age')
    assert response.status_code == 200
    assert response.data.index(b"John") < response.data.index(b"Lisa")

    # Проверяем сортировку и фильтрацию одновременно
    response = client.get('/data?filename=test_file.csv&column=Age&value=25&sort_by=Last Name')
    assert response.status_code == 200
    assert b"Johnson" in response.data
    assert b"Doe" in response.data
    assert response.data.index(b"Johnson") > response.data.index(b"Doe")


def run_tests():
    pytest.main()

if __name__ == '__main__':
    run_tests()