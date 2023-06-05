# Musicnextdoor

Welcome to the MusicNextDoor! This is a platform where music enthusiasts can connect, share their favorite albums, write reviews, and engage in discussions with other users. Every user can write a review and discuss about their favorite albums. It offers separate implementations using Django and FastAPI to cater to different preferences and requirements

## Features

- User Registration and Login: Users can sign up and create an account to access all the features of the web application.
- Voting: Users can vote for their favorite albums and share their opinions on the quality and appeal of the music.
- Album Reviews: Users can write detailed reviews and share their thoughts on their favorite albums.
- Comments and Chat: Users can engage in chat-like discussions by commenting on posts and interacting with other users.

## Getting Started

1. Clone the repository to your local machine.
2. Install the required dependencies using `pipenv install -r requirements.txt`.
3. Set up the database and perform migrations using `python manage.py migrate`.
4. Start the development server with `python manage.py runserver`.
5. Access the Music Blog in your web browser at `http://localhost:8000`.
6. Access FastAPI backend code seperately: exit previous virtual environment `deactivate`
7.  Navigate to the fastapi directory: `cd ..` then `cd musicnextdoor-fastapi`
8. create a virtual environment `pipenv shell`
9. install dependecies `pipenv install -r requirements.txt`
10. start the development server `uvicorn main:app --reload`
11. Access the app in your browser at `http://localhost:8000`

## User Registration

To access all the features of the Music Blog, users need to create an account. Follow these steps to register:

1. On the homepage, click on the "Sign Up" link.
2. Fill in the registration form with your desired username, email, and password.
3. Click the "Register" button to create your account.

## User Login

If you already have an account, follow these steps to log in:

1. On the homepage, click on the "Sign In" link.
2. Enter your username and password in the login form.
3. Click the "Log In" button to access your account.

## Voting

To vote for your favorite albums, follow these steps:

1. Find the album you want to vote for.
2. Click on the "Vote" button.
3. Select your vote.
4. Submit your vote to have your opinion counted.

## Album Reviews

To write a review for your favorite album, follow these steps:

1. Click on the "Write Review".
2. Provide your detailed review, sharing your thoughts and opinions on an album.
3. Submit your review to share it with other users.

## Comments and Chat

To engage in discussions and chat with other users, follow these steps:

1. Scroll through the posts and find the one you want to comment on.
2. Click on the "Comment" section or a similar feature associated with the post.
3. Type your comment in the provided input field.
4. Submit your comment to participate in the conversation.

## Contributing

We welcome contributions from the community to enhance the Music Blog. If you would like to contribute, please follow these steps:

1. Fork the repository and create your branch for development.
2. Make your changes and additions.
3. Test your changes to ensure they do not introduce any issues.
4. Commit your changes with clear and descriptive commit messages.
5. Push your changes to your forked repository.
6. Submit a pull request detailing the changes you have made.
