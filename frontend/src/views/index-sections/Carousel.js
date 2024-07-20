import React, { useEffect, useState } from "react";
import { styled, Grid, Card, CardContent, Typography, CircularProgress, FormControlLabel, Checkbox, Button, Box, TextField } from '@mui/material';
import { Container, Row, Col, Carousel, CarouselItem, CarouselIndicators } from "reactstrap";
import 'D:/weekend/frontend/src/assets/css/MostFavoritedCocktails.css';
import { useTransition, animated } from '@react-spring/web';

const id = localStorage.getItem("userId");

const getImageSrc = (id) => {
  try {
    return require(`D:/weekend/frontend/src/assets/img/${id}.jpg`);
  } catch (err) {
    console.error(`Image not found for cocktail ID: ${id}`);
    return null; // Return null if image is not found
  }
};

const CarouselSection = () => {
  const [cocktails, setCocktails] = useState([]);
  const [items, setItems] = useState([]);
  const [comments, setComments] = useState([]);
  const [activeIndex, setActiveIndex] = useState(0);
  const [animating, setAnimating] = useState(false);

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
        console.log("Fetched most favorited cocktails:", data);
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
        console.log("Fetched cocktail details:", cocktailDetails);
        setCocktails(cocktailDetails);
        const carouselItems = cocktailDetails.map(cocktail => ({
          src: getImageSrc(cocktail['ID of Cocktail']),
          altText: cocktail['Name of Cocktail'],
          caption: cocktail['English Name of Cocktail']
        }));
        console.log("Carousel items:", carouselItems);
        setItems(carouselItems);
        if (cocktailDetails.length > 0) {
          setComments(cocktailDetails[0].comments || []);
        }
      })
      .catch(error => {
        console.error('Error fetching cocktail details:', error);
      });
  }, [id]); // Ensure id is defined and correct

  const onExiting = () => {
    setAnimating(true);
  };

  const onExited = () => {
    setAnimating(false);
  };

  const next = () => {
    if (animating) return;
    const nextIndex = activeIndex === items.length - 1 ? 0 : activeIndex + 1;
    setActiveIndex(nextIndex);
    setComments(cocktails[nextIndex].comments || []);
  };

  const previous = () => {
    if (animating) return;
    const nextIndex = activeIndex === 0 ? items.length - 1 : activeIndex - 1;
    setActiveIndex(nextIndex);
    setComments(cocktails[nextIndex].comments || []);
  };

  const goToIndex = (newIndex) => {
    if (animating) return;
    setActiveIndex(newIndex);
    setComments(cocktails[newIndex].comments || []);
  };

  return (
    <div className="section" id="carousel">
      <Container>
        <div className="title" align="center">
          <h2>Most Favorited Cocktails</h2>
        </div>
        <Row className="justify-content-center">
          <Col lg="8" md="12">
            <div style={{ display: 'flex', justifyContent: 'center', gap: '20px' }}>
              <div style={{ flex: '1' }}>
                <Carousel
                  activeIndex={activeIndex}
                  next={next}
                  previous={previous}
                  style={{ width: '400px', height: '400px' }}
                >
                  {items.map((item, index) => (
                    <CarouselItem
                      onExiting={onExiting}
                      onExited={onExited}
                      key={index}
                    >
                      <img src={item.src} alt={item.altText} style={{ width: '400px', height: '400px' }} />
                      <div className="carousel-caption d-none d-md-block">
                        <h5>{item.caption}</h5>
                      </div>
                    </CarouselItem>
                  ))}
                  <a
                    className="carousel-control-prev"
                    data-slide="prev"
                    href="#pablo"
                    onClick={(e) => {
                      e.preventDefault();
                      previous();
                    }}
                    role="button"
                  >
                    <i className="now-ui-icons arrows-1_minimal-left"></i>
                  </a>
                  <a
                    className="carousel-control-next"
                    data-slide="next"
                    href="#pablo"
                    onClick={(e) => {
                      e.preventDefault();
                      next();
                    }}
                    role="button"
                  >
                    <i className="now-ui-icons arrows-1_minimal-right"></i>
                  </a>
                </Carousel>
              </div>
              <div style={{ flex: '1', maxHeight: '400px', overflowY: 'auto' }}>
                {comments.map((comment, index) => (
                  <Card key={index} style={{ marginBottom: '20px', boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)'}}>
                    <CardContent>
                      <Typography>{comment.Message}</Typography>
                      <Typography className="mb-2 text-muted">{comment.time}</Typography>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default CarouselSection;
