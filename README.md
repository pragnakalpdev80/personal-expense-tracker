# deepgram-tts


### Requirements

- Python 3.12+ (Django 5.2 LTS)
- PostgreSQL 15+
- Redis 7+


### Installation

```bash
# 1. Navigate to the backend directory
cd personal-expense-tracker/

# 2. Create and activate virtual environment
# Standard Python 3.12+ is supported
python3 -m venv venv

source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create environment file
cp .env.example .env
# Edit .env with your actual values

# 5. Run database migrations
python3 manage.py migrate

# 6. Create a superuser (admin account)
python3 manage.py createsuperuser

# 7. Start the development server
python3 manage.py runserver