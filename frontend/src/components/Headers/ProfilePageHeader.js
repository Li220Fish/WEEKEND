import React, { useState, useEffect, useRef } from "react";
import { Container, Col, Row } from "reactstrap";
import { useNavigate } from 'react-router-dom';

function ProfilePageHeader() {
  const [username, setUserName] = useState("USER");
  const [userlike, setUserLike] = useState("0");
  const [usercomment, setUserComment] = useState("0");
  const [userstore, setUserStore] = useState("0");
  const pageHeader = useRef();
  const navigate = useNavigate();
  const [cart, setCart] = useState([]);
  const [cartCount, setCartCount] = useState(0);

  useEffect(() => {
    const storedCart = JSON.parse(localStorage.getItem('cart')) || [];
    setCart(storedCart);
    setCartCount(storedCart.length); // Update cart count
  }, []);

  useEffect(() => {
    const getInfo = async () => {
      const id = localStorage.getItem("userId");
      const response = await fetch('/info', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id })
      });

      if (response.ok) {
        const data = await response.json();
        console.log(data);
        setUserName(data.username);
        localStorage.setItem("userName", data.username);
        setUserLike(data.like);
        setUserComment(data.comment);
        setUserStore(cartCount); // Correctly set the cart count
        console.log(username, userlike, usercomment);
      } else {
        console.error('Error:', response.statusText);
      }
    };

    getInfo();

    if (window.innerWidth > 991) {
      const updateScroll = () => {
        let windowScrollTop = window.pageYOffset / 3;
        pageHeader.current.style.transform =
          "translate3d(0," + windowScrollTop + "px,0)";
      };
      window.addEventListener("scroll", updateScroll);
      return function cleanup() {
        window.removeEventListener("scroll", updateScroll);
      };
    }
  }, [cartCount]); // Add cartCount to dependency array

  return (
    <>
      <div
        className="page-header clear-filter page-header-small"
        filter-color="blue"
      >
        <div
          className="page-header-image"
          style={{
            backgroundImage: "url(" + require("assets/img/bg11.jpg") + ")"
          }}
          ref={pageHeader}
        ></div>
        <Container>
          <h3 className="title">{username}</h3>
          <p className="category">Information</p>
          <Row>
            <Col>
              <h2>{userlike}</h2>
              <p>Like</p>
            </Col>
            <Col>
              <h2>{usercomment}</h2>
              <p>Comments</p>
            </Col>
            <Col>
              <h2>{userstore}</h2>
              <p>Store</p>
            </Col>
          </Row>
        </Container>
      </div>
    </>
  );
}

export default ProfilePageHeader;
