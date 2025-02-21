# Learning Assistant

**Learning Assistant** is a Django-based platform designed for students to manage and interact with AI models. Users can upload API keys from various chatbot service providers or create their own AI models with customized prompts, configurations, and development tools.

## 🚧 Project Status: Under Development
This project is still in its early stages, and many features are under development. We appreciate any contributions, feedback, and suggestions to help improve the project.

## Features (Planned and In-Progress)
- Upload API keys from chatbot providers.
- Create and manage AI models.
- Customize prompts and model configurations.
- Develop tools for AI models.
- PostgreSQL database with `pgvector` support for vector embeddings.

## Prerequisites
Before running the project, ensure you have:
- Docker and Docker Compose installed
- Python 3.8+
- PostgreSQL (if running without Docker)

## Installation and Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Ali619/learning-assistant.git
cd learning-assistant
```

### 2. Setup Environment Variables
Rename `.env.copy` to `.env` and update the values accordingly:
```bash
mv .env.copy .env
```
Edit the `.env` file with your database credentials:
```
SECRET_KEY=your_django_secret_key
DATABASE_HOST=localhost  # Change to "postgres" if using Docker
DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
DATABASE_PASS=your_db_password
DATABASE_PORT=5432
```

### 3. Start PostgreSQL with Docker and Install pgvector
Run the following command to start PostgreSQL and pgAdmin:
```bash
docker-compose up -d
```
Once the database is running, connect to PostgreSQL and install the `pgvector` extension:

---
You need to create the pgvector extension in your PostgreSQL database first. Since we're using Django with a PostgreSQL database, you have two options:

**1. Create a migration to install the extension:**

Create a new migration file (you can name it something like `0002_create_vector_extension.py` in your app's migrations folder):

```python
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        # Replace 'your_app' with your app name and the previous migration
        ('your_app', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            "CREATE EXTENSION IF NOT EXISTS vector",
            "DROP EXTENSION IF EXISTS vector"
        )
    ]
```
**2. Or connect to your database directly and create the extension:** (Using psql command line)
```bash
psql -h localhost -U postgres -d postgres
```
Then run:
```sql
CREATE EXTENSION vector;
```

After creating the extension, run your migrations again:
```bash
python manage.py migrate
```

This will start:
- **PostgreSQL** on port `5432`
- **pgAdmin** on `http://localhost:5050` (Login: `admin@example.com`, Password: `admin`)

### 4. Install Python Dependencies
Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Create a Superuser (Optional)
If you need admin access:
```bash
python manage.py createsuperuser
```

### 7. Start the Django Server
```bash
python manage.py runserver
```
The project will be accessible at `http://127.0.0.1:8000/`

## Accessing pgAdmin
You can access **pgAdmin** at `http://localhost:5050/` with the following credentials:
- **Email**: `admin@example.com`
- **Password**: `admin`

To connect pgAdmin to the PostgreSQL database:
1. Navigate to `Servers > Create > Server`
2. Under **General**, set a name (e.g., `LearningAssistantDB`)
3. Under **Connection**:
   - **Host**: `postgres` (if using Docker) or `localhost`
   - **Port**: `5432`
   - **Username**: `postgres`
   - **Password**: `password`

## Stopping the Project
To stop the running services:
```bash
docker-compose down
```
To stop the Django server, press `CTRL + C` in the terminal.

## Contributing
We welcome contributions to this project! Since the project is still under development, here are some ways you can help:
1. Report bugs and suggest features by opening an issue.
2. Fork the repository and submit pull requests with improvements.
3. Help refine the documentation as new features are added.

If you're interested in contributing, feel free to reach out!

## License
This project is licensed under the MIT License. See `LICENSE` for details.

---

### Need Help?
If you encounter any issues, feel free to open an issue in the repository or reach out to the maintainers.

---
**Happy coding! 🚀**

