# PythonMVC

This is a self-built python MVC framework which can be used for web applications with a WSGI web server, such as Gunicorn.

Order of events to return content to the user:

1. User requests resource via web browser
2. WSGI server initiates python app
3. **Request** is processed and all relevant fields are saved
4. **Dispatcher** processes the request to identify required **Controller**
5. If the required **Controller** is found, desired method is executed.
6. Error is shown if **Controller** is not found
7. **Controller** method requests data from **Model** and return the output from **View**
8. Output is rendered on the user's browser