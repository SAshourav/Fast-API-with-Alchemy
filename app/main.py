from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

        
@app.get('/posts')
def test_posts(db: Session = Depends(get_db)):
    
    post = db.query(models.Post).all()
    return {"data": post}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    try:
        # new_post = models.Post(title=post.title, content=post.content, published=post.published)
        new_post = models.Post(**post.dict())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return {"data": new_post}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get('/posts/{id}')
def get_post(id: int, db: Session = Depends(get_db)):
    try:
        # Query the post by ID
        post = db.query(models.Post).filter(models.Post.id == id).first()
        
        # Check if the post was found
        if not post:
            raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
        
        return {"data": post}
    
    except Exception as e:
        # Catch any unexpected errors and raise a 500 error
        raise HTTPException(status_code=500, detail=str(e))

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    try:
        post = db.query(models.Post).filter(models.Post.id == id)
        if post.first() == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"post with id:{id} does not exist ")
        post.delete(synchronize_session=False)
        db.commit()
    except Exception as e:
        # Catch any unexpected errors and raise a 500 error
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from . import models
from .database import get_db

app = FastAPI()

@app.put('/posts/{id}', status_code=status.HTTP_200_OK)
def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    existing_post = post_query.first()
    
    if existing_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    # Use `post.dict()` with `exclude_unset=True` to only update fields provided in the request body
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    # Return the updated post
    return {"data": post_query.first()}
