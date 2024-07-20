/*eslint-disable*/
import React from "react";

// reactstrap components
import { Container } from "reactstrap";

function TransparentFooter() {
  return (
    <footer className="footer">
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
          <a
            target="_blank"
          >
            9 Group
          </a>
          . Coded by{" "}
          <a
            target="_blank"
          >
            Team Member
          </a>
          .
        </div>
      </Container>
    </footer>
  );
}

export default TransparentFooter;
