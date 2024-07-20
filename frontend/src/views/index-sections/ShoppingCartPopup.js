import React, { useEffect, useState } from 'react';
import { Typography, Box, Button, Card, CardContent } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import 'D:/weekend/frontend/src/assets/css/ShoppingCartPopup.css'; // Ensure you use the correct path
import { Link } from 'react-router-dom';

const u_id = localStorage.getItem("userId");

const ShoppingCartPopup = ({ onClose, isOpen }) => {
    const [cart, setCart] = useState([]);
    const [cocktails, setCocktails] = useState([]);

    useEffect(() => {
        const fetchCartData = () => {
            const storedCart = JSON.parse(localStorage.getItem('cart')) || [];
            setCart(storedCart);
            fetchCocktails(storedCart);
        };

        fetchCartData();

        // Listen for changes in local storage
        const handleStorageChange = () => {
            fetchCartData();
        };

        window.addEventListener('storage', handleStorageChange);

        return () => {
            window.removeEventListener('storage', handleStorageChange);
        };
    }, []);

    const fetchCocktails = (cartItems) => {
        Promise.all(cartItems.map(id => 
            fetch(`/api/cocktails/${id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({user_id: u_id })
            })
            .then(response => response.json())
        ))
        .then(data => {
            setCocktails(data);
        })
        .catch(error => {
            console.error('Error fetching cocktails:', error);
        });
    };

    const handleRemoveFromCart = (id) => {
        const updatedCart = cart.filter(itemId => itemId !== id);
        localStorage.setItem('cart', JSON.stringify(updatedCart));
        setCart(updatedCart);
        fetchCocktails(updatedCart);
    };

    const getImageSrc = (id) => {
        try {
            return require(`D:/weekend/frontend/src/assets/img/${id}.jpg`);
        } catch (err) {
            console.error(`Image not found for cocktail ID: ${id}`);
            return null;
        }
    };

    return (
        <div className={`shopping-popup-cart-popup ${isOpen ? 'active' : ''}`}>
            <div className="shopping-popup-cart-header">
                <Typography variant="h6">Wish List</Typography>
                <Button className="close-btn" onClick={onClose}>
                    <CloseIcon />
                </Button>
            </div>
            <Box className="popup-cart-container">
                <div className="popup-cart-content">
                    <div className="popup-cart-left-flex">
                        {cocktails.length > 0 ? (
                            cocktails.map(cocktail => (
                                <Card key={cocktail['ID of Cocktail']} className="popup-cart-card">
                                    <CardContent className="popup-cart-card-content">
                                        <div className="popup-cart-cocktail-image-container">
                                            {getImageSrc(`${cocktail['ID of Cocktail']}`) ? (
                                                <img src={getImageSrc(`${cocktail['ID of Cocktail']}`)} className="popup-cart-image" alt={cocktail['Name of Cocktail']} />
                                            ) : (
                                                'Image not available'
                                            )}
                                        </div>
                                        <div className="popup-cart-cocktail-details">
                                            <Typography className="popup-cart-cocktail-name" variant="body2" component="p">
                                                {cocktail['Name of Cocktail']}
                                            </Typography>
                                            <Typography className="popup-cart-cocktail-english-name" variant="body2" component="p">
                                                {cocktail['English Name of Cocktail']}
                                            </Typography>
                                        </div>
                                        <Button
                                            aria-label="remove"
                                            className="popup-cart-remove-button"
                                            onClick={() => handleRemoveFromCart(cocktail['ID of Cocktail'])}
                                        >
                                            <CloseIcon />
                                        </Button>
                                    </CardContent>
                                </Card>
                            ))
                        ) : (
                            <Typography className="popup-cart-empty-message">No items in the cart.</Typography>
                        )}
                    </div>
                    <Link to="/like-page" className="detail-button">
                        Click For Details
                    </Link>
                </div>
            </Box>
        </div>
    );
};

export default ShoppingCartPopup;
