import React, { useEffect, useState } from 'react';
import { Typography, Box, Button, Card, CardContent } from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import CloseIcon from '@mui/icons-material/Close';
import { useNavigate } from 'react-router-dom';
import 'D:/weekend/frontend/src/assets/css/ShoppingCartPage.css';

const ShoppingCartPage = () => {
    const [cart, setCart] = useState([]);
    const navigate = useNavigate();
    const [cocktails, setCocktails] = useState([]);
    const [ingredients, setIngredients] = useState(new Set());
    const u_id = localStorage.getItem('userId');


    useEffect(() => {
        const storedCart = JSON.parse(localStorage.getItem('cart')) || [];
        setCart(storedCart);
        fetchCocktails(storedCart);
        fetchAllIngredients(storedCart);
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
    const fetchAllIngredients = (cartItems) => {
        const ingredientMap = new Map();
    
        Promise.all(cartItems.map(id => fetch(`/api/cocktails/${id}/ingredients`)
            .then(response => response.json())))
            .then(data => {
                data.forEach(item => {
                    /*if (item['name of wine']) {
                        const wineName = item['name of wine'];
                        if (!ingredientMap.has(wineName)) {
                            ingredientMap.set(wineName, { amount: '1' }); // Assuming the whole bottle is used
                        } else {
                            const currentAmount = ingredientMap.get(wineName).amount;
                            ingredientMap.set(wineName, { amount: `${parseInt(currentAmount) + 1}` });
                        }
                    }*/
                    item.ingredients.forEach(ingredient => {
                        const ingredientName = ingredient['Name of Ingredients'];
                        const convertedAmount = convertToML(ingredient['Amount of Used']);
                        if (!ingredientMap.has(ingredientName)) {
                            if (!isNaN(convertedAmount)) {
                                ingredientMap.set(ingredientName, { amount: `${convertedAmount} mL` });
                            } else {
                                ingredientMap.set(ingredientName, { amount: convertedAmount });
                            }
                        } else {
                            const currentAmount = ingredientMap.get(ingredientName).amount;
                            // Check if both current and converted amounts are numeric
                            const currentNumericAmount = parseFloat(currentAmount.replace(/[^0-9.]/g, ''));
                            const convertedNumericAmount = parseFloat(convertedAmount);
                            if (!isNaN(currentNumericAmount) && !isNaN(convertedNumericAmount)) {
                                ingredientMap.set(ingredientName, { amount: (currentNumericAmount + convertedNumericAmount).toFixed(2) + ' mL' });
                            } else {
                                // If either is not numeric, concatenate with a comma
                                ingredientMap.set(ingredientName, { amount: `${currentAmount},${convertedAmount}` });
                            }
                        }
                    });
                });
    
                // Convert ingredientMap to a set format required for rendering
                const ingredientSet = new Set();
                ingredientMap.forEach((value, key) => {
                    ingredientSet.add(`${key} (${value.amount})`);
                });
    
                setIngredients(ingredientSet);
            })
            .catch(error => {
                console.error('Error fetching ingredients:', error);
            });
    };
    
    const convertToML = (amountStr) => {
        let amount = parseFloat(amountStr.replace(/[^0-9.]/g, ''));
        if (isNaN(amount)) {
            return amountStr; // return original string if conversion fails
        }
        if (amountStr.includes('tsb')) {
            return (amount * 14.79).toFixed(2); // return numeric value in mL
        } else if (amountStr.includes('dash')) {
            return (amount * 0.625).toFixed(2); // return numeric value in mL
        } else if (amountStr.includes('tsp')) {
            return (amount * 4.93).toFixed(2); // return numeric value in mL
        } else if (amountStr.includes('mL') || amountStr.includes('ml')) {
            return amount.toFixed(2); // return numeric value in mL
        } else {
            return amountStr; // return original string if no conversion needed
        }
    };

    const handleRemoveFromCart = (id) => {
        const updatedCart = cart.filter(itemId => itemId !== id);
        localStorage.setItem('cart', JSON.stringify(updatedCart));
        setCart(updatedCart);
        fetchCocktails(updatedCart);
        fetchAllIngredients(updatedCart);
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
        <div>
            <Box className="cart-container">
                <Typography variant="h4" className="cart-title">Shopping Cart</Typography>
                <div className="cart-content">
                    <div className="cart-left-flex">
                        {cocktails.length > 0 ? (
                            cocktails.map(cocktail => (
                                <Card key={cocktail['ID of Cocktail']} className="cart-card">
                                    <CardContent className="cart-card-content">
                                        <div className="cart-cocktail-image-container">
                                            {getImageSrc(`${cocktail['ID of Cocktail']}`) ? (
                                                <img src={getImageSrc(`${cocktail['ID of Cocktail']}`)} className="cart-image" />
                                            ) : (
                                                'Image not available'
                                            )}
                                        </div>
                                        <div className="cart-cocktail-details">
                                            <Typography className="cart-cocktail-name" variant="body2" component="p">
                                                {cocktail['Name of Cocktail']}
                                            </Typography>
                                            <Typography className="cart-cocktail-english-name" variant="body2" component="p">
                                                {cocktail['English Name of Cocktail']}
                                            </Typography>
                                        </div>
                                        <Button
                                            aria-label="remove"
                                            className="cart-remove-button"
                                            onClick={() => handleRemoveFromCart(cocktail['ID of Cocktail'])}
                                        >
                                            <CloseIcon />
                                        </Button>
                                    </CardContent>
                                </Card>
                            ))
                        ) : (
                            <Typography className="cart-empty-message">No items in the cart.</Typography>
                        )}
                    </div>
                    <div className="cart-right-flex">
                        <Card className="cart-summary-card">
                            <CardContent>
                                <Typography variant="h6">Order Summary</Typography>
                                <div className="order-summary-content">
                                    {[...ingredients].map((ingredient, index) => (
                                        <Box key={index} p={1} mb={1} border={1} borderColor="grey.300" className='Ingredient-box'>
                                            <Typography variant="body2" component="p">
                                                {ingredient.split(' (')[0]}
                                            </Typography>
                                            <Typography variant="body2" component="p" style={{ textAlign: 'right' }}>
                                                ({ingredient.split(' (')[1]})
                                            </Typography>
                                        </Box>
                                    ))}
                                </div>
                            </CardContent>
                        </Card>
                    </div>
                </div>
            </Box>
        </div>
    );
};

export default ShoppingCartPage;
