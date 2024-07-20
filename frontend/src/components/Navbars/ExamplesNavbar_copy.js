import React from "react";
import { Link } from "react-router-dom";
import {
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
  const [isCartOpen, setIsCartOpen] = React.useState(false);

  const handleCartToggle = () => {
    setIsCartOpen((prevState) => !prevState);
  };

  return (
    <>
      <Navbar className={"fixed-top " + navbarColor} color="info" expand="lg">
        <Container>
          <div className="navbar-translate">
            <NavbarBrand target="_blank" id="navbar-brand">
              WEEKEND
            </NavbarBrand>
            <UncontrolledTooltip target="#navbar-brand">
              have a few drink!
            </UncontrolledTooltip>
          </div>
          <Nav className="ml-auto" navbar>
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
          </Nav>
        </Container>
      </Navbar>
      <ShoppingCartPopup isOpen={isCartOpen} onClose={handleCartToggle} />
    </>
  );
}

export default ExamplesNavbar;
