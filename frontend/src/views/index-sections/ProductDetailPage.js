import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Typography, Button, TextField, Box } from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import ThumbUpIcon from '@mui/icons-material/ThumbUp';
import 'D:/weekend/frontend/src/assets/css/ProductDetailPage.css'; // Ensure you use the correct path
import { Link } from 'react-router-dom';
import { ChatBubble } from '@mui/icons-material';
import ChatPopup from './ChatPopup'; // Import the ChatPopup component
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
import ShoppingCartPopup from './ShoppingCartPopup';
import ExamplesNavbarcopy from 'components/Navbars/ExamplesNavbar_copy';
import {
    Input,
    InputGroupAddon,
    InputGroupText,
    InputGroup,
    Container,
    Row,
    Col
  } from "reactstrap";

const ProductDetailPage = () => {
    //cart
    const [isCartOpen, setIsCartOpen] = useState(false);

    const handleCartToggle = () => {
        setIsCartOpen(prevState => !prevState);
    };
    //

    // chat
    const [isChatOpen, setIsChatOpen] = useState(false); // State to track if the chat window is open

    const handleCloseChat = () => {
        setIsChatOpen(false);
    };
    // chat

    const { productId } = useParams();
    const navigate = useNavigate();
    const [cocktail, setCocktail] = useState(null);
    const [error, setError] = useState(null);
    const [comment, setComment] = useState('');
    const [msgUser, setMsgUser] = useState('');
    const [comments, setComments] = useState([]);
    const [liked, setLiked] = useState(false); // Initialize like state
    const [userId, setUserId] = useState("");
    const id = localStorage.getItem("userId");
    const user = localStorage.getItem("userName");
    

    //ingredients
    const [ingredients, setIngredients] = useState(null);

    // Function to determine alcohol concentration
    const getAlcoholConcentration = (high, medium, low) => {
        if (high == 1) {
            return 'High';
        } else if (medium == 1) {
            return 'Medium';
        } else if (low == 1) {
            return 'Low';
        }
        return 'Unknown'; // Handle other cases or return a default value
    };

    const getTaste = (sour, sweet, bitter, spicy) => {
        let taste = '';
        if (sour == 1) {
            taste += 'Sour ';
        }
        if (sweet == 1) {
            taste += 'Sweet ';
        }
        if (bitter == 1) {
            taste += 'Bitter ';
        }
        if (spicy == 1) {
            taste += 'Spicy';
        }
        return taste.trim();
    };

    const getTemperature = (ice, hot) => {
        if (ice == 1) {
            return 'Cold';
        } else if (hot == 1) {
            return 'Hot';
        }
        return 'Unknown'; // Handle other cases or return a default value
    };

    const handleLike = () => {
        if (id === null) {
            alert('You need to sign in first');
            return;
        }else{
    
        console.log(id);
        const url = liked
            ? `/api/cocktails/${productId}/unlike`
            : `/api/cocktails/${productId}/like`;
    
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ action: liked ? 'unlike' : 'like', user_id: id })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            setLiked(!liked);
            setCocktail(prevState => ({
                ...prevState,
                likes: liked ? prevState.likes - 1 : prevState.likes + 1
            }));
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
    };
    

    const handleCommentChange = (event) => {
        setComment(event.target.value);
    };

    const handleCommentSubmit = () => {
        if (id === null) {
            alert('You need to sign in first');
            return;
        } else{
    
        fetch(`/api/cocktails/${productId}/comment`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: comment, user_id: id })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok'); 
            }
            return response.json();
        })
        .then(data => {
            const currentDate = new Date();
            const year = currentDate.getFullYear();
            const month = currentDate.getMonth() + 1;
            const day = currentDate.getDate();
            const hours = currentDate.getHours();
            const minutes = currentDate.getMinutes();
            const formattedDate = `${year}-${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')} ${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
            
            setComments([...comments, { User_name: data.user_name, Message: comment, time: formattedDate }]);
            setComment(''); // Clear the comment input
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
    };
    

    useEffect(() => {
        fetch(`/api/cocktails/${productId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({user_id: id})
        })
            .then(response => {
                console.log('Response status:', response.status);
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Fetched data:', data);
                setCocktail(data);
                setComments(data.comments || []);
                setLiked(data.is_liked || false); // Set initial liked state
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                setError('An error occurred while fetching data.');
            });

        // Fetch ingredients
        fetch(`/api/cocktails/${productId}/ingredients`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(response => {
                console.log('Ingredients response status:', response.status);
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Fetched ingredients:', data);
                setIngredients(data);
            })
            .catch(error => {
                console.error('Error fetching ingredients:', error);
                setError('An error occurred while fetching ingredients.');
            });

    }, [productId]);

    const handleAddToCart = () => {
        if (id === null) {
            alert('You need to sign in first');
            return;
        } else{
        let cart = JSON.parse(localStorage.getItem('cart')) || [];
        if (!cart.includes(productId)) {
            cart.push(productId);
            localStorage.setItem('cart', JSON.stringify(cart)); 
            console.log(cart);
            alert('Added to cart!');
            window.location.reload(); // Reload the page
        } else {
            alert('Already in cart');
        }
    }
    };

    const getImageSrc = () => {
        try {
            return require(`D:/weekend/frontend/src/assets/img/${cocktail['ID of Cocktail']}.jpg`);
        } catch (err) {
            console.error(`Image not found for cocktail ID: ${cocktail['ID of Cocktail']}`);
            return null; // Return null if image is not found
        }
    };

    if (error) {
        return <div>{error}</div>;
    }

    return (
        <>
        <ExamplesNavbarcopy/>
        <div>
            {/* chat*/}
            <div>
                <button className="chat-button" onClick={() => setIsChatOpen(true)}><ChatBubble /></button>
                {isChatOpen && <ChatPopup onClose={handleCloseChat} />} {/* Pass the onClose function as a prop */}
                
                <button></button>{/* useless*/}
            </div>
            {/* chat*/}

            <Box className="new_container">
                {cocktail ? (
                    <Box className="new_flex-container">
                        <Box className="left-section">

                            <Box className="image-placeholder">
                                {getImageSrc() ? (
                                    <img src={getImageSrc()}/>
                                ) : (
                                    'Image not available'
                                )}
                            </Box>

                        </Box>
                        <Box className="new_right-section">
                            <Typography variant="h4">{cocktail['Name of Cocktail']}</Typography>
                            <Typography variant="h6" style={{ fontSize: '30px' }}>{cocktail['English Name of Cocktail']}</Typography>
                            <Typography>Production Method: {cocktail['Production Method']}</Typography>
                            <Typography>Alcohol concentration: {getAlcoholConcentration(cocktail['High alcohol concentration'], cocktail['Medium alcohol concentration'], cocktail['Low alcohol concentration'])}</Typography>
                            <Typography>Tastes: {getTaste(cocktail['Sour'], cocktail['Sweet'], cocktail['Bitter'], cocktail['Spicy'])}</Typography>
                            <Typography>Hot or Cold: {getTemperature(cocktail['Ice'], cocktail['Hot'])}</Typography>
                            <Box className="like-container">
                                <Button
                                    variant="contained"
                                    style={{ backgroundColor: liked ? 'green' : 'black', color: 'white' }} // Change color based on liked state
                                    onClick={handleLike}
                                    className="like-button"
                                >
                                    <ThumbUpIcon />
                                </Button>
                                <Typography>Likes: {cocktail.likes}</Typography> {/* Adjusted like count display */}

                                <Button
                                    variant="contained"
                                    style={{ backgroundColor: 'orange', color: 'white', marginLeft: '10px' }}
                                    onClick={handleAddToCart}
                                    className="cart-button"
                                >
                                    <ShoppingCartIcon />
                                </Button>
                            </Box>
                        </Box>

                        {/* Ingredients Section */}
                        <Box className="ingredient-section">
                            {ingredients && (
                                <Box className="ingredients-section">
                                    <Typography variant="h4">Ingredients</Typography>
                                    <Typography>Name of Wine: {ingredients['name of wine']}</Typography>
                                    <Typography>Name of Ingredients and Amount:</Typography>
                                    {ingredients.ingredients.map((ingredient, index) => (
                                        <Box key={index} className="ingredient-box">
                                            <Typography>{ingredient['Name of Ingredients']} {ingredient['Amount of Used']}</Typography>
                                        </Box>
                                    ))}
                                </Box>
                            )}
                        </Box>

                    </Box>
                ) : (
                    <Typography variant="h6">Loading...</Typography>
                )}


                <Box className="comments-section">
                    <Typography variant="h5">Comments</Typography>
                    {comments.map((comment, index) => (
                        <Box key={index} className="comment-box">
                            <Typography>User name: {comment.User_name}</Typography>
                            <Typography>Message: {comment.Message}</Typography>
                            <Typography>Time: {comment.time}</Typography>
                        </Box>
                    ))}
                    <TextField
                        label="Add a comment"
                        value={comment}
                        onChange={handleCommentChange}
                        fullWidth
                        variant="outlined"
                        margin="normal"
                    />
                    <Button variant="contained" color="primary" onClick={handleCommentSubmit}>
                        Add Comment
                    </Button>
                </Box>

            </Box>
        </div>
    </>
    );
};

export default ProductDetailPage;
