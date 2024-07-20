import React, { useEffect, useState } from 'react';
import { styled,Grid, Card, CardContent, Typography, CircularProgress, FormControlLabel, Checkbox, Button, Box, TextField,IconButton } from '@mui/material';
import { FormControl, RadioGroup, Radio } from '@mui/material';
import { ChatBubble } from '@mui/icons-material';
import ChatPopup from './ChatPopup'; // Import the ChatPopup component
import { ExpandMore, ExpandLess } from '@mui/icons-material';

import { Link } from 'react-router-dom';
import 'D:/weekend/frontend/src/assets/css/App.css';  // Import CSS for styling

const CocktailImage = styled('img')({
    width: '100%',
    height: 'auto',
    borderRadius: '8px',
  });

const CocktailTable = () => {

    // chat
    const [isChatOpen, setIsChatOpen] = useState(false); // State to track if the chat window is open

    const handleCloseChat = () => {
        setIsChatOpen(false);
    };
    // chat
    const [cocktail, setCocktail] = useState(null);
    const [cocktails, setCocktails] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [filters, setFilters] = useState({
        highAlcohol: false,
        mediumAlcohol: false,
        lowAlcohol: false,
        sour: false,
        sweet: false,
        bitter: false,
        spicy: false,
        ice: false,
        hot: false,
        A01: false,
        A02: false,
        A03: false,
        A04: false,
        A05: false,
        A06: false,
        A07: false,
    });

    const [searchText, setSearchText] = useState('');
    const [currentPage, setCurrentPage] = useState(1);
    const itemsPerPage = 15;
    const [isFilterExpanded, setIsFilterExpanded] = useState(false); // State to track filter visibility

    useEffect(() => {
        fetch('/api/cocktails', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
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
                setCocktails(data);
                setLoading(false);
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                setError('An error occurred while fetching data.');
                setLoading(false);
            });
    }, []);

    const getImageSrc = (get_Id) => {
        try {
          return require(`D:/weekend/frontend/src/assets/img/${get_Id}.jpg`);
        } catch (err) {
          console.error(`Image not found for cocktail ID: ${get_Id}`);
          return null; // Return null if image is not found
        }
      };

    const handleFilterChange = (event) => {
        const { name, checked } = event.target;
    
        setFilters(prevFilters => {
            let newFilters = { ...prevFilters, [name]: checked };
    
            if (name === 'highAlcohol' || name === 'mediumAlcohol' || name === 'lowAlcohol') {
                // If an alcohol concentration checkbox is checked, uncheck the others
                newFilters = {
                    ...newFilters,
                    highAlcohol: name === 'highAlcohol' ? checked : false,
                    mediumAlcohol: name === 'mediumAlcohol' ? checked : false,
                    lowAlcohol: name === 'lowAlcohol' ? checked : false,
                };
            }
    
            if (name === 'sour' || name === 'sweet' || name === 'bitter' || name === 'spicy') {
                // If a taste checkbox is checked, uncheck the others
                newFilters = {
                    ...newFilters,
                    sour: name === 'sour' ? checked : false,
                    sweet: name === 'sweet' ? checked : false,
                    bitter: name === 'bitter' ? checked : false,
                    spicy: name === 'spicy' ? checked : false,
                };
            }
    
            if (name === 'ice' || name === 'hot') {
                // If a hot or cold checkbox is checked, uncheck the other
                newFilters = {
                    ...newFilters,
                    ice: name === 'ice' ? checked : false,
                    hot: name === 'hot' ? checked : false,
                };
            }
    
            return newFilters;
        });
        setCurrentPage(1);
    };
    

    const handleSearchChange = (event) => {
        setSearchText(event.target.value.toLowerCase());
        setCurrentPage(1);
    };

    const filterCocktails = (cocktail) => {
    const {
        highAlcohol, mediumAlcohol, lowAlcohol, sour, sweet, bitter, spicy, ice, hot,
        A01, A02, A03, A04, A05, A06, A07
    } = filters;

    const filterConditions = [
        { filter: highAlcohol, key: 'High alcohol concentration' },
        { filter: mediumAlcohol, key: 'Medium alcohol concentration' },
        { filter: lowAlcohol, key: 'Low alcohol concentration' },
        { filter: sour, key: 'Sour' },
        { filter: sweet, key: 'Sweet' },
        { filter: bitter, key: 'Bitter' },
        { filter: spicy, key: 'Spicy' },
        { filter: ice, key: 'Ice' },
        { filter: hot, key: 'Hot' },
    ];

    // Liquor filter conditions
    const liquorFilters = [
        { filter: A01, key: 'A01' },
        { filter: A02, key: 'A02' },
        { filter: A03, key: 'A03' },
        { filter: A04, key: 'A04' },
        { filter: A05, key: 'A05' },
        { filter: A06, key: 'A06' },
        { filter: A07, key: 'A07' },
    ];

    // Check if any filter is active
    const isAnyFilterActive = filterConditions.some(condition => condition.filter) ||
                              liquorFilters.some(condition => condition.filter);

    if (!isAnyFilterActive && searchText === "") {
        return true;
    }

    const meetsFilterConditions = filterConditions.every(condition => !condition.filter || cocktail[condition.key] == 1);
    const meetsLiquorFilterConditions = liquorFilters.some(condition => condition.filter && cocktail['ID of Liquor'] === condition.key);

    const nameOfCocktail = cocktail['Name of Cocktail'] ? cocktail['Name of Cocktail'].toLowerCase() : "";
    const englishNameOfCocktail = cocktail['English Name of Cocktail'] ? cocktail['English Name of Cocktail'].toLowerCase() : "";

    return meetsFilterConditions && 
           (liquorFilters.every(condition => !condition.filter) || meetsLiquorFilterConditions) &&
           (searchText === "" ||
            nameOfCocktail.includes(searchText) ||
            englishNameOfCocktail.includes(searchText));
};


    const filteredCocktails = cocktails.filter(filterCocktails);

    const handleNextPage = () => {
        setCurrentPage(currentPage + 1);
    };

    const handlePreviousPage = () => {
        setCurrentPage(currentPage - 1);
    };

    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const currentCocktails = filteredCocktails.slice(startIndex, endIndex);
    const totalPages = Math.ceil(filteredCocktails.length / itemsPerPage);

    if (loading) {
        return <CircularProgress />;
    }

    if (error) {
        return <div>{error}</div>;
    }

    if (cocktails.length === 0) {
        return <div>No cocktails available</div>;
    }

    return (
        <div section id="cocktail_mode">
        
        {/* chat8*/}
        <div>
            <button className="chat-button" onClick={() => setIsChatOpen(true)}><ChatBubble /></button>
            {isChatOpen && <ChatPopup onClose={handleCloseChat} />} {/* Pass the onClose function as a prop */}
        </div>
        {/* chat8*/}
        <div className='list-header'>
                <h2
                    align="center"
                    style={{ margin: '40px 0'}}
                >
                    Cocktail List
                </h2>
            </div>

        <div className="cocktail-table-container">
        <div className="sidebar">
                    <Typography className="filter-section">
                        Filter
                        <IconButton onClick={() => setIsFilterExpanded(!isFilterExpanded)}>
                            {isFilterExpanded ? <ExpandLess /> : <ExpandMore />}
                        </IconButton>
                    </Typography>

                    <div className={`filter-options ${isFilterExpanded ? 'expanded' : ''}`}>
                        <TextField
                            label="Search"
                            variant="outlined"
                            fullWidth
                            value={searchText}
                            onChange={handleSearchChange}
                        />
                        <Typography className="alcohol-section">Alcohol Concentration </Typography>
                        <FormControlLabel
                            control={
                                <Checkbox
                                    checked={filters.highAlcohol}
                                    onChange={handleFilterChange}
                                    name="highAlcohol"
                                />
                            }
                            label="High"
                        />
                        <FormControlLabel
                            control={
                                <Checkbox
                                    checked={filters.mediumAlcohol}
                                    onChange={handleFilterChange}
                                    name="mediumAlcohol"
                                />
                            }
                            label="Medium"
                        />
                        <FormControlLabel
                            control={
                                <Checkbox
                                    checked={filters.lowAlcohol}
                                    onChange={handleFilterChange}
                                    name="lowAlcohol"
                                />
                            }
                            label="Low"
                        />
                        <Typography className="taste-section">Tastes </Typography>
                        <FormControlLabel
                            control={
                                <Checkbox
                                    checked={filters.sour}
                                    onChange={handleFilterChange}
                                    name="sour"
                                />
                            }
                            label="Sour"
                        />
                        <FormControlLabel
                            control={
                                <Checkbox
                                    checked={filters.sweet}
                                    onChange={handleFilterChange}
                                    name="sweet"
                                />
                            }
                            label="Sweet"
                        />
                        <FormControlLabel
                            control={
                                <Checkbox
                                    checked={filters.bitter}
                                    onChange={handleFilterChange}
                                    name="bitter"
                                />
                            }
                            label="Bitter"
                        />
                        <FormControlLabel
                            control={
                                <Checkbox
                                    checked={filters.spicy}
                                    onChange={handleFilterChange}
                                    name="spicy"
                                />
                            }
                            label="Spicy"
                        />
                        <Typography className="hot-cold-section">Hot or Cold </Typography>
                        <FormControlLabel
                            control={
                                <Checkbox
                                    checked={filters.ice}
                                    onChange={handleFilterChange}
                                    name="ice"
                                />
                            }
                            label="Ice"
                        />
                        <FormControlLabel
                            control={
                                <Checkbox
                                    checked={filters.hot}
                                    onChange={handleFilterChange}
                                    name="hot"
                                />
                            }
                            label="Hot"
                        />
                        <Typography className="liquor-section">Liquor ID</Typography>
                        <FormControlLabel
                            control={
                                <Checkbox
                                    checked={filters.A01}
                                    onChange={handleFilterChange}
                                    name="A01"
                                />
                            }
                            label="Vodka"
                        />
                        <FormControlLabel
                            control={
                                <Checkbox
                                    checked={filters.A02}
                                    onChange={handleFilterChange}
                                    name="A02"
                                />
                            }
                            label="Rum"
                        />
                        <FormControlLabel
                            control={
                                <Checkbox
                                    checked={filters.A03}
                                    onChange={handleFilterChange}
                                    name="A03"
                                />
                            }
                            label="Brandy"
                        />
                        <FormControlLabel
                            control={
                                <Checkbox
                                    checked={filters.A04}
                                    onChange={handleFilterChange}
                                    name="A04"
                                />
                            }
                            label="Liqueur"
                        />
                        <FormControlLabel
                            control={
                                <Checkbox
                                    checked={filters.A05}
                                    onChange={handleFilterChange}
                                    name="A05"
                                />
                            }
                            label="Gin"
                        />
                        <FormControlLabel
                            control={
                                <Checkbox
                                    checked={filters.A06}
                                    onChange={handleFilterChange}
                                    name="A06"
                                />
                            }
                            label="Tequila"
                        />
                        <FormControlLabel
                            control={
                                <Checkbox
                                    checked={filters.A07}
                                    onChange={handleFilterChange}
                                    name="A07"
                                />
                            }
                            label="Whiskey"
                        />

                    </div>
                </div>
            
            <div className="new_content">
                <Grid container spacing={4}>
                    {currentCocktails.map(cocktail => (
                        <Grid item key={cocktail['ID of Cocktail']} xs={12} sm={6} md={4}>
                            <Card component={Link} to={`/products/${cocktail['ID of Cocktail']}`}>
                                <CardContent className="card-content">
                                    <Box className="cocktail-image-wrapper">
                                        
                                        {getImageSrc(cocktail['ID of Cocktail']) ? (
                                            <img src={getImageSrc(cocktail['ID of Cocktail'])}/>
                                        ) : (
                                            <h4>{cocktail['ID of Cocktail']}</h4>
                                                
                                        )}
                                    </Box>
                                    <Typography className="cocktail-name" variant="body2" component="p">
                                        {cocktail['Name of Cocktail']}
                                    </Typography>
                                    <Typography className="cocktail-english-name" variant="body2" component="p">
                                        {cocktail['English Name of Cocktail']}
                                    </Typography>
                                </CardContent>
                            </Card>
                        </Grid>
                    ))}
                </Grid>
            </div>

            

        </div>
            <div className="pagination">
                <Button variant="contained" color="primary" onClick={handlePreviousPage} disabled={currentPage === 1}>
                    Previous
                </Button>
                <Typography className="page-info">Page {currentPage} of {totalPages}</Typography>
                <Button variant="contained" color="primary" onClick={handleNextPage} disabled={endIndex >= filteredCocktails.length}>
                    Next
                </Button>
            </div>

        </div>
    );
};

export default CocktailTable;
