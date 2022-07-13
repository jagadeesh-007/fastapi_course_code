from unittest import result
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
import models, schemas, oauth2
from typing import List, Optional
from sqlalchemy.orm import Session
from database import  engine, get_db
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags = ['Posts'] 
)

# requests Get all the values method url: "/posts"
# @router.get("/", response_model=List[schemas.Post])
@router.get("/")
def get_posts(db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10, skip: int = 0, search: Optional[str]= ""):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    print(search)
  
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
        models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    
    return  posts

# To insert value to the database
@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post : schemas.PostCreate, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title, content, published)
    #                VALUES (%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # using **post.dict to convert into a dict
    # and also using this we can avoid typing mulitple columns
    new_posts = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)
    return new_posts

# #  to get the latest value
# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts)-1]
#     print(post)
#     return {"detail":  post}

# To get single value based on the ID
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id : int, response : Response, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.id == id).first()
    
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found "}
    
 
    return  post

# To Delete a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *  """, (str(id),))
    # deleted_post = cursor.fetchone() 
    # conn.commit() 
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if  post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id: {id} does not exist")
        
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perfrom requested action")
     
    post_query.delete(synchronize_session=False)
    db.commit()
    
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#test connection with database
# @app.get("/sqlalchemy")
# def test_post(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all
    
#     return {"Data": posts}

#To update the database
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s  WHERE id = %s RETURNING * """, 
    #                (post.title, post.content, post.published, str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id )
    post = post_query.first()
    if  post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id: {id} does not exist")
        
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perfrom requested action")
    
        
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    return post_query.first()