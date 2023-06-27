import { useState, useEffect } from "react"
import CommentForm from './CommentForm'

function CommentsContainer({post_id, user_id}){
    const [comments, setComments] = useState([])
    const [liked, setLiked] = useState(false)
    useEffect(() => {
        fetch('http://localhost:3000/comments')
        .then(r => r.json())
        .then(data => setComments(data))
        .catch(err => console.error(err))
    })

    const handleSubmitComment = (e, submitComment) => {
        e.preventDefault()
        fetch('http://localhost:3000/comments', {
            method: 'POST',
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(submitComment)
        }).then(res => res.json())
        .then(comment => setComments(current => [...current, comment]))
        .catch(err => console.error(err))
    }

    const handleLiked = () => {
        setLiked(current => !current)
    }

    return(
        <div className="comments">
            <CommentForm handleSubmitComment={handleSubmitComment}/>
            <div>
            {comments.map(comment => {
                return (<div className="comment">
                    <img className="comment-photo" src={comment['image_uri']}/>
                    <div className='comment-text'>{comment[text]}</div>
                    <button onClick={handleLiked}>
                        {liked ? <div className="unlike">Heart</div> : <div className='like'>Heart</div>}
                    </button>
                </div>)
            })}
            </div>
        </div>
    )
}

export default CommentsContainer;