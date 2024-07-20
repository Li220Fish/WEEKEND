import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Grid, Card, CardContent, Typography, IconButton } from '@mui/material';
import { ChevronLeft, ChevronRight } from '@mui/icons-material';
import 'D:/weekend/frontend/src/assets/css/MostFavoritedCocktails.css';
const id = localStorage.getItem("userId");


const getImageSrc = (id) => {
    try {
        return require(`D:/weekend/frontend/src/assets/img/${id}.jpg`);
    } catch (err) {
        console.error(`Image not found for cocktail ID: ${id}`);
        return null; // Return null if image is not found
    }
};

const MostFavoritedCocktails = () => {
    const [cocktails, setCocktails] = useState([]);
    const [currentIndex, setCurrentIndex] = useState(0);
    const itemsPerPage = 3;

    useEffect(() => {
        fetch('/api/most_favorited_cocktails', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                const fetchCocktailDetails = data.map(favorite =>
                    fetch(`/api/cocktails/${favorite['ID of Cocktail']}`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ user_id: id })
                    })
                        .then(response => {
                            if (!response.ok) {
                                throw new Error('Network response was not ok');
                            }
                            return response.json();
                        })
                );
    
                return Promise.all(fetchCocktailDetails);
            })
            .then(cocktailDetails => {
                setCocktails(cocktailDetails);
            })
            .catch(error => {
                console.error('Error fetching cocktail details:', error);
            });
    }, [id]); // Ensure id is defined and correct
    

    const handleNext = () => {
        const newIndex = currentIndex + itemsPerPage;
        if (newIndex < cocktails.length) {
            setCurrentIndex(newIndex);
        }
    };

    const handlePrev = () => {
        const newIndex = currentIndex - itemsPerPage;
        if (newIndex >= 0) {
            setCurrentIndex(newIndex);
        }
    };

    return (
        <div className="most-favorited-container">
            <div className="most-favorited-header">
                <Typography variant="h6" component="h2">
                    Most Favorited Cocktails
                </Typography>
            </div>
            <div className="most-favorited-content">
                <IconButton className="most-favorited-arrow-button" onClick={handlePrev} disabled={currentIndex === 0}>
                    <ChevronLeft />
                </IconButton>
                <Grid container spacing={3}>
                    {cocktails.slice(currentIndex, currentIndex + itemsPerPage).map(cocktail => (
                        <Grid item key={cocktail['ID of Cocktail']} xs={12} sm={6} md={4}>
                            <Card component={Link} to={`/products/${cocktail['ID of Cocktail']}`}>
                                <CardContent className="most-favorited-card-content">
                                    <div className="most-favorited-cocktail-image">
                                        {getImageSrc(cocktail['ID of Cocktail']) ? (
                                            <img src={getImageSrc(cocktail['ID of Cocktail'])} alt={cocktail['Name of Cocktail']} />
                                        ) : (
                                            'Image not available'
                                        )}
                                    </div>
                                    <Typography className="most-favorited-cocktail-name" >
                                        {cocktail['Name of Cocktail']}
                                    </Typography>
                                    <Typography className="most-favorited-cocktail-english-name" >
                                        {cocktail['English Name of Cocktail']}
                                    </Typography>
                                </CardContent>
                            </Card>
                        </Grid>
                    ))}
                </Grid>
                <IconButton className="most-favorited-arrow-button" onClick={handleNext} disabled={currentIndex + itemsPerPage >= cocktails.length}>
                    <ChevronRight />
                </IconButton>
            </div>
        </div>
    );
};

export default MostFavoritedCocktails;
