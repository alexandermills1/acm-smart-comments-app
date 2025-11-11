# acm-smart-comments-app
Developer hiring challenge - Smart Comments App

Build instructions
	Prerequisites**:  
	- Python 3.10+
	- Node.js 18+ (includes npm)  
	- PostgreSQL (running locally)  
	- Git (to clone the repo)
	
	
	Terminal 1:
		*move to directory you want to download project*
		git clone https://github.com/alexandermills1/acm-smart-comments-app.git
		code .
		cd frontend
		npm install
		npm run watch
			(places frontend build into `backend/static`)
	
	Terminal 2:
		psql postgres
		CREATE DATABASE smartcomments;
		\q
	
		cd backend
		python3 -m venv venv
		source venv/bin/activate 
			# (Windows: venv\Scripts\activate)
		pip install -r requirements.txt
		python manage.py migrate
		python manage.py runserver


Create a post
Create a comment to the post
Flagged comments will be sent to Moderator page for review
easy test: short comments will "need review", try "hi"


Architechture and design choices
Backend
	- Django + Django REST Framework (DRF) for API backend  
	- Class-based views with DRF generics for CRUD operations  
	- Single-app structure (`smart_comments`) with models, views, serializers, urls  
	- Static `index.html` served directly from Django for React SPA  
	- Rule-based comment classifier (`classifier.py) runs synchronously on comment creation
Frontend
	- React Router, custom hooks (`usePosts`, `useFlaggedComments`), Axios for API calls  
	- Moderator page shows only flagged comments 
	- New posts/comments added instantly without refresh

AI integration approach:
	None

How'd you scale, test, and monitor system
- scale: distributed event streaming platform 
- test: none (would add pytest)
- monitor: none (would add logs)

Any improvements you'd make with more time
- Improve styling
- Integrate OpenAI API for text-classification model
- Added testing
- create docker file
