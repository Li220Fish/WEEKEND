import React from "react";
import { Link } from "react-router-dom";
import {
  Collapse,
  NavbarBrand,
  Navbar,
  NavItem,
  NavLink,
  Nav,
  Container,
  UncontrolledTooltip,
} from "reactstrap";
import ShoppingCartPopup from "views/index-sections/ShoppingCartPopup";

function ExamplesNavbar() {
  const [navbarColor, setNavbarColor] = React.useState("");
  const [collapseOpen, setCollapseOpen] = React.useState(false);
  const [isCartOpen, setIsCartOpen] = React.useState(false);

  const handleCartToggle = () => {
    setIsCartOpen((prevState) => !prevState);
  };

  return (
    <>
      {collapseOpen ? (
        <div
          id="bodyClick"
          onClick={() => {
            document.documentElement.classList.toggle("nav-open");
            setCollapseOpen(false);
          }}
        />
      ) : null}
      <Navbar className={"fixed-top " + navbarColor} color="info" expand="lg">
        <Container>
          <div className="navbar-translate">
            <NavbarBrand target="_blank" id="navbar-brand">
              WEEKEND
            </NavbarBrand>
            <UncontrolledTooltip target="#navbar-brand">
              have a few drink!
            </UncontrolledTooltip>
            <button
              className="navbar-toggler navbar-toggler"
              onClick={() => {
                document.documentElement.classList.toggle("nav-open");
                setCollapseOpen(!collapseOpen);
              }}
              aria-expanded={collapseOpen}
              type="button"
            >
              <span className="navbar-toggler-bar top-bar"></span>
              <span className="navbar-toggler-bar middle-bar"></span>
              <span className="navbar-toggler-bar bottom-bar"></span>
            </button>
          </div>
          <Collapse className="justify-content-end" isOpen={collapseOpen} navbar>
            <Nav navbar>
              <NavItem>
                <NavLink to="/index" tag={Link}>
                  Back to home
                </NavLink>
              </NavItem>
              
              <NavItem>
                <NavLink onClick={handleCartToggle}>
                  Store cart
                </NavLink>
              </NavItem>

              <NavItem>
                <NavLink href="https://github.com/Li220Fish/Webp2024/issues">
                  Have an issue?
                </NavLink>
              </NavItem>
            </Nav>
          </Collapse>
        </Container>
      </Navbar>
      <ShoppingCartPopup isOpen={isCartOpen} onClose={handleCartToggle} />
    </>
  );
}

export default ExamplesNavbar;
