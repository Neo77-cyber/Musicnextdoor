from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.fastapi import register_tortoise
import random
from pydantic import BaseModel, Field
from tortoise.exceptions import DoesNotExist
from tortoise.contrib.pydantic import pydantic_model_creator
from datetime import datetime
from typing import Dict





app = FastAPI()

SECRET_KEY = "pD2-Oi5DYtgMEE642AMPtn6NmRdrshqZ5XAA3oNBoJE"

ACCESS_TOKEN_EXPIRE_MINUTES = 1440

password_context = CryptContext(schemes=['bcrypt'], deprecated = "auto")   


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length = 100)
    password_hash = fields.CharField(max_length = 100)

    async def verify_password(self, plain_password):
        return password_context.hash(plain_password)
    
    class PydanticMeta:
        exclude = ["password_hash"]

VOTE_CHOICES = (
    ('i\m adding this to my playlist', 'I\'M ADDING THIS TO MY PLAYLIST'),
    ('good but no replay value', 'GOOD BUT NO REPLAY VALUE'),
    ('meh put it in a trash', 'MEH PUT THIS IN A TRASH'),
)

class BlogPost(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE)
    title = fields.CharField(max_length=200)
    body = fields.CharField(max_length=200)
    post_date = fields.DatetimeField(auto_now_add=True)
    vote_counts = fields.JSONField(null=True)  # New field for storing vote counts
    vote_percentages = fields.JSONField(null=True) 

class Comment(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE)
    blogpost = fields.ForeignKeyField("models.BlogPost", on_delete=fields.CASCADE)
    comment = fields.CharField(max_length=200)
    created_at = fields.DatetimeField(auto_now_add=True)

class Vote(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE)
    blogpost = fields.ForeignKeyField("models.BlogPost", on_delete=fields.CASCADE)
    vote = fields.CharField(max_length=200, choices=VOTE_CHOICES, default = 'i\m adding this to my playlist')

BlogPostPydantic = pydantic_model_creator(BlogPost)


class BlogPostCreateRequest(BaseModel):
    title: str
    body: str
    post_date_time: datetime = Field(default_factory=datetime.utcnow)


class BlogPostResponse(BaseModel):
    user: str
    title: str
    body: str
    post_date_time: datetime
    vote_counts: Dict[str, int] = Field(default_factory=dict)
    vote_percentages: Dict[str, float] = Field(default_factory=dict)

class CommentCreateRequest(BaseModel):
    blogpost_id: int
    comment: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class CommentResponse(BaseModel):
    id: int
    user: str
    blogpost_id: int
    comment: str
    created_at: datetime

class VoteCreateRequest(BaseModel):
    blogpost_id: int
    vote: str

class VoteResponse(BaseModel):
    id: int
    user: str
    blogpost_id: int
    vote: str
    vote_counts: Dict[str, int] = Field(default_factory=dict)
    vote_percentages: Dict[str, float] = Field(default_factory=dict)


register_tortoise(
    app,
    db_url='sqlite:///Users/neo/Documents/Codez/FASTApipractice/voteblog/database.db',
    modules={'models': ['main']},
    generate_schemas=True,
    add_exception_handlers=True,
)

async def get_user(username: str):
    return await User.get_or_none(username=username)

def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)

def authenticate_user(user:User, password: str):
    if not user or not verify_password(password, user.password_hash):
        return False
    else:
        return user
    
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post('/register')
async def register(username:str, password:str):
    existing_user = await get_user(username)
    if existing_user:
        raise HTTPException(status_code = 400, detail = 'Username already exists')
    hashed_password = password_context.hash(password)
    user = await User.create(username=username, password_hash = hashed_password)
    return {"message": "Registered successfuly"}

@app.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user(form_data.username)
    if not user or not await user.verify_password(form_data.password):
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub": user.username}, access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

    
@app.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        user = await get_user(username)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token.")
        return {"message": "Protected route accessed successfully."}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")
    
@app.post("/token")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user(form_data.username)
    if not user or not await user.verify_password(form_data.password):
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub": user.username}, access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/create_post", response_model = BlogPostResponse)
async def create_post(new_post:BlogPostCreateRequest, token:str = Depends(oauth2_scheme)):
    try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            username = payload.get("sub")
            user = await get_user(username)
            print(user)
            if not user:
                raise HTTPException(status_code=401, detail="Invalid token.")
            create_post = await BlogPost.create(user=user, title=new_post.title, body=new_post.body,
                                            post_date=new_post.post_date_time)

            response = BlogPostResponse(user=user.username, title=new_post.title, body=new_post.body,
                                    post_date_time=new_post.post_date_time, vote_counts={},vote_percentages={})
            return response

    except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token.")
    

@app.post("/create_comment", response_model = CommentResponse)
async def create_comment(new_comment:CommentCreateRequest, token:str = Depends(oauth2_scheme)):
    try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            username = payload.get("sub")
            user = await get_user(username)
            if not user:
                raise HTTPException(status_code=401, detail="Invalid token.")
            blogpost = await BlogPost.get_or_none(id=new_comment.blogpost_id)
            if not blogpost:
                raise HTTPException(status_code=404, detail="Blog post not found.")

            comment = await Comment.create(user=user, blogpost=blogpost, comment=new_comment.comment,
                                       created_at=new_comment.created_at)

            response = CommentResponse(
                id=comment.id,
                user=user.username,
                blogpost_id=blogpost.id,
                comment=comment.comment,
                created_at=comment.created_at
            )
            return response

    except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token.")
    
@app.post("/vote", response_model=VoteResponse)
async def create_vote(new_vote: VoteCreateRequest, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        user = await get_user(username)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token.")

        blogpost = await BlogPost.get_or_none(id=new_vote.blogpost_id)
        if not blogpost:
            raise HTTPException(status_code=404, detail="Blog post not found.")

        vote = await Vote.create(user=user, blogpost=blogpost, vote=new_vote.vote)

        vote_counts = {choice[0]: 0 for choice in VOTE_CHOICES}
        votes = await Vote.filter(blogpost=blogpost)
        for v in votes:
            vote_counts[v.vote] += 1

        
        total_votes = len(votes)
        vote_percentages = {choice: count / total_votes * 100 if total_votes > 0 else 0 for choice, count in vote_counts.items()}

        response = VoteResponse(
            id=vote.id,
            user=user.username,
            blogpost_id=blogpost.id,
            vote=vote.vote,
        )

        response.vote_counts = vote_counts
        response.vote_percentages = vote_percentages

        return response

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")