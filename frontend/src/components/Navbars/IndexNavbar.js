import React from "react";
import { Link } from "react-router-dom";
import {
  Button,
  Collapse,
  DropdownToggle,
  DropdownMenu,
  DropdownItem,
  UncontrolledDropdown,
  NavbarBrand,
  Navbar,
  NavItem,
  NavLink,
  Nav,
  Container,
  UncontrolledTooltip,
} from "reactstrap";
import { Link as ScrollLink, animateScroll as scroll } from 'react-scroll';

function IndexNavbar() {
  const [navbarColor, setNavbarColor] = React.useState("navbar-transparent");
  const [collapseOpen, setCollapseOpen] = React.useState(false);

  const [username, setUserName] = React.useState("USER");
  const [userlike, setUserLike] = React.useState("0");
  const [usercomment, setUserComment] = React.useState("0");
  const [userstore, setUserStore] = React.useState("0");

  React.useEffect(() => {

    const getInfo = async () => {
      const id = localStorage.getItem("userId");
      console.log(id);
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
        console.log(username, userlike, usercomment);
      } else {
        console.error('Error:', response.statusText);
      }
    };

    getInfo();

    const updateNavbarColor = () => {
      if (
        document.documentElement.scrollTop > 399 ||
        document.body.scrollTop > 399
      ) {
        setNavbarColor("");
      } else if (
        document.documentElement.scrollTop < 400 ||
        document.body.scrollTop < 400
      ) {
        setNavbarColor("navbar-transparent");
      }
    };
    window.addEventListener("scroll", updateNavbarColor);
    return function cleanup() {
      window.removeEventListener("scroll", updateNavbarColor);
    };
  }, []);
  
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
      <Navbar className={"fixed-top " + navbarColor} expand="lg" color="info">
        <Container>
          <div className="navbar-translate">
            <NavbarBrand
              target="_blank"
              id="navbar-brand"
            >
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
          <Collapse
            className="justify-content-end"
            isOpen={collapseOpen}
            navbar
          >
            <Nav navbar>
              <NavItem>
                <ScrollLink
                  to="introduction_mode"
                  smooth={true}
                  duration={500}
                  className="nav-link"
                >
                  <i className="now-ui-icons text_bold"></i>
                  <p>Introduction</p>
                </ScrollLink>
              </NavItem>

              <NavItem>
                <ScrollLink
                  to="cocktail_mode"
                  smooth={true}
                  duration={500}
                  className="nav-link"
                >
                  <i className="now-ui-icons files_paper"></i>
                  <p>Cocktail List</p>
                </ScrollLink>
              </NavItem>

              <NavItem>
                <ScrollLink
                  to="specials-section"
                  smooth={true}
                  duration={500}
                  className="nav-link"
                >
                  <i className="now-ui-icons sport_trophy"></i>
                  <p>Popular Specials</p>
                </ScrollLink>
              </NavItem>

              <UncontrolledDropdown nav>
                <DropdownToggle
                  caret
                  color="default"
                  href="#pablo"
                  nav
                  onClick={(e) => e.preventDefault()}
                >
                  <i className="now-ui-icons users_single-02"></i>
                  <p>Account</p>
                </DropdownToggle>
                <DropdownMenu>
                  <DropdownItem
                    to="/like-page"
                    outline
                    tag={Link}>
                    <i className="now-ui-icons ui-2_favourite-28"></i>
                    Like Cocktail
                  </DropdownItem>

                  <DropdownItem
                    to="/profile-page"
                    outline
                    tag={Link}
                  >
                    <i className="now-ui-icons ui-1_settings-gear-63"></i>
                    Setting
                  </DropdownItem>

                  <DropdownItem
                    to="/login-page"
                    outline
                    tag={Link}
                  >
                    <i className="now-ui-icons users_circle-08"></i>
                    Login / Signup
                  </DropdownItem>
                </DropdownMenu>
              </UncontrolledDropdown>
            </Nav>
          </Collapse>
        </Container>
      </Navbar>
    </>
  );
}

export default IndexNavbar;
