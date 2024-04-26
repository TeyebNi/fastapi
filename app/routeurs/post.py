from .. import models,schemas,Utils 
from fastapi import HTTPException, status,Response,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import   List , Optional

from .. import database , oauth2
from sqlalchemy import func


router = APIRouter(
    prefix="/posts" ,
    tags=['Posts']
)



@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
   # cursor.execute("""SELECT * FROM posts""")
   # posts = cursor.fetchall()
   
  # posts = db.query(models.Post).all()
#    posts = db.query(models.Post).filter(
#        models.Post.title.contains(search)).limit(limit).offset( skip).all()
   


#    posts = db.query(models.Post , func.count(models.Vote.post_id).label("votes")).join(
#        models.Vote , models.Vote.post_id == models.Post.id,
#        isouter= True).group_by(models.Post.id).filter(
#            models.Post.title.contains(search)).limit(limit).offset(skip).all()
   
#    return posts
  posts = db.query(models.Post).filter(
    models.Post.title.contains(search)).limit(limit).offset(skip).all()
    

  resultats = db.query(models.Post , func.count(models.Vote.post_id).label("votes")).join(
      models.Vote , models.Vote.post_id == models.Post.id,
      isouter= True).group_by(models.Post.id).filter(
      models.Post.title.contains(search)).limit(limit).offset(skip).all()

  return resultats

  




@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,db : Session = Depends(get_db) ,
                   current_user : int  = Depends(oauth2.get_current_user) ):
    #cursor.execute(f"""INSERT INTO posts(title,content,published) Values(%s,%s,%s) RETURNING * """,
                #   (post.title,post.content,post.published))
   # new_posts = cursor.fetchone()

    #conn.commit()
    #print(current_user.id)
    #print(current_user.email) 
    new_posts = models.Post(owner_id = current_user.id , **post.dict())
    #**dict bdl mn (title=post.title,content=post.content,published=post.published )

#pour ajouter ou inserter les donnee en postgres
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)
    return new_posts

@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id:int , db : Session = Depends(get_db) , current_user : int = Depends(oauth2.get_current_user) ):
    #cursor.execute("""SELECT * FROM posts where id = %s """,(str(id)))
    #post = cursor.fetchone()

    # post =  db.query(models.Post).filter(models.Post.id == id).first()
    
    post = db.query(models.Post , func.count(models.Vote.post_id).label("votes")).join(
      models.Vote , models.Vote.post_id == models.Post.id,
      isouter= True).group_by(models.Post.id).filter(models.Post.id == id).first()

   
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")

    return post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db : Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):

    #cursor.execute("""DELETE FROM posts WHERE id = %s returning *""",(str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()



    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException (status_code=status.HTTP_403_FORBIDDEN ,
                              detail= " Not authorized to perform requeusted action")
    
    post_query.delete(synchronize_session = False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int , updated_post : schemas.PostCreate,db : Session = Depends(get_db) , current_user : int  = Depends(oauth2.get_current_user)):

   # cursor.execute("""UPDATE posts SET title = %s , content = %s,published = %s WhERE id = %s RETURNING *""",
                 #  (post.title,post.content,post.published,str(id)))

    #updated_post = cursor.fetchone()
    #conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    
    if post == None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,
                             detail="post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException (status_code=status.HTTP_403_FORBIDDEN ,
                              detail= " Not authorized to perform requeusted action")
    
    post_query.update(updated_post.dict(),synchronize_session=False)
    #dict bdl mn {'title': 'Hey this is mmy updated title','content':'This is my updated content'}
    db.commit()
    return post_query.first()