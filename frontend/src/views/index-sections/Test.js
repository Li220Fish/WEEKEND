import React from "react";
import { Link } from "react-router-dom";
// reactstrap components
import { Button, Container, Row } from "reactstrap";

// core components

function Examples() {
  return (
    <>
    
      <div className="section section-examples" data-background-color="black" section id="introduction_mode">
      
        <div className="space-50"></div>
        <Container className="text-center">
        <h2>About This Website</h2>
          <Row>
            <div className="col">
                <h5>
                  <p align="left">
                  On this website, you will be able to find various cocktail recipes.
                  After logging in, you can share your valuable ideas and preferences 
                  with other users on the site. Additionally, we have an exclusive bot
                  that can provide you with real-time suggestions.
                  </p>
                </h5>
            </div>
            
            <div className="col"> 
                <img
                  alt="..."
                  className="img-raised"
                  src={require("assets/img/profile.jpg")}
                ></img>
            </div>
          </Row>
        </Container>
      </div>

    </>
  );
}

export default Examples;
