    
Test the API: You can use Postman or cURL to test the API endpoints.
        Register a user:
            POST /register
            Body: {"username": "your_username", "password": "your_password"}
        Login:
            POST /login
            Body: {"username": "your_username", "password": "your_password"}
        Manage notes:
            Create Note: POST /notes
                Body: {"title": "Note Title", "content": "Note Content"}
            Get Notes: GET /notes
            Update Note: PUT /notes/<note_id>
                Body: {"title": "Updated Title", "content": "Updated Content"}
            Delete Note: DELETE /notes/<note_id>

