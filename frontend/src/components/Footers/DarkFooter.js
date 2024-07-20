/*eslint-disable*/
import React from "react";

// reactstrap components
import { Container } from "reactstrap";

function DarkFooter() {
  return (
    <footer className="footer" data-background-color="black">
      <Container>
        <nav>
          <ul>
            <li>
              <a
                href="https://github.com/Li220Fish"
                target="_blank"
              >
                Li_Fish
              </a>
            </li>
          </ul>
        </nav>
        <div className="copyright" id="copyright">
          © {new Date().getFullYear()}, Designed by{" "}
          <a>
            9 Group
          </a>
          . Coded by{" "}
          <a>
            Team Member
          </a>
          .
        </div>
      </Container>
    </footer>
  );
}

export default DarkFooter;
