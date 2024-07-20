import React from "react";
import { useNavigate } from 'react-router-dom';
import { useHistory } from "react-router-dom";

// reactstrap components
import {
  Button,
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  Form,
  Input,
  InputGroupAddon,
  InputGroupText,
  InputGroup,
  Container,
  Col,
} from "reactstrap";

// core components
import LoginNavbar from "components/Navbars/LoginNavbar.js";
import TransparentFooter from "components/Footers/TransparentFooter.js";

function LoginPage() {
  const [firstFocus, setFirstFocus] = React.useState(false);
  const [lastFocus, setLastFocus] = React.useState(false);
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');
  const navigate = useNavigate();

  React.useEffect(() => {
    document.body.classList.add("login-page");
    document.body.classList.add("sidebar-collapse");
    document.documentElement.classList.remove("nav-open");
    window.scrollTo(0, 0);
    document.body.scrollTop = 0;
    return function cleanup() {
      document.body.classList.remove("login-page");
      document.body.classList.remove("sidebar-collapse");
    };
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if(email ===""){
      alert("your email can't be empty");
    }else if(password ===""){
      alert("your password can't be empty");
    }else{
     const response = await fetch('/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
    });

    if (response.ok) {
      const data = await response.json();
      console.log('Success:', data);
      if (data.message ==="成功登入!"){
        localStorage.setItem("userId", data.user_id);
        navigate('/index');
      }else if(data.message ==="帳號不存在"){
        alert("帳號不存在，請輸入Gmail後，按下Create按鍵");
      }
    } else {
      console.error('Error:', response.statusText);
    }
    }
  };

  const [isButtonLocked, setIsButtonLocked] = React.useState(false);

  const handleCreateAccount = async (e) => {
    e.preventDefault();
    if (email === "") {
      alert("Your email can't be empty");
    } else if (isButtonLocked) {
      alert('Wait 10 seconds');
    } else {
      const response = await fetch('/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email })
      });

      if (response.ok) {
        const data = await response.json();
        console.log('Account creation success:', data);
        alert('An email has been sent to your Gmail');
        setIsButtonLocked(true);
        setTimeout(() => {
          setIsButtonLocked(false);
        }, 10000);
      } else {
        console.error('Account creation error:', response.statusText);
      }
    }
  };

  const [isForgetButtonLocked, setIsForgetButtonLocked] = React.useState(false);
  const handleForgetAccount = async (e) => {
    e.preventDefault();
    if(email ===""){
      alert("your email can't be empty");
    }else if (isForgetButtonLocked) {
      alert('Wait 10 seconds');
    }else{
      const response = await fetch('/forget', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email })
      });
    
      if (response.ok) {
        const data = await response.json();
        console.log('Account creation success:', data);
        alert('An email has been sent to your Gmail');
        setIsForgetButtonLocked(true);
        setTimeout(() => {
          setIsForgetButtonLocked(false);
        }, 10000);
      } else {
        console.error('Account creation error:', response.statusText);
      }
    }
  };

  return (
    <>
      <LoginNavbar />
      <div className="page-header clear-filter" filter-color="blue">
        <div
          className="page-header-image"
          style={{
            backgroundImage: "url(" + require("assets/img/login.jpg") + ")"
          }}
        ></div>
        <div className="content">
          <Container>
            <Col className="ml-auto mr-auto" md="4">
              <Card className="card-login card-plain">
                <Form className="form" onSubmit={handleSubmit}>
                  <CardHeader className="text-center">
                    <div className="logo-container">
                      <img
                        alt="..."
                        src={require("assets/img/now-logo.png")}
                      ></img>
                    </div>
                  </CardHeader>
                  <CardBody>
                    <InputGroup
                      className={
                        "no-border input-lg" +
                        (firstFocus ? " input-group-focus" : "")
                      }
                    >
                      <InputGroupAddon addonType="prepend">
                        <InputGroupText>
                          <i className="now-ui-icons users_circle-08"></i>
                        </InputGroupText>
                      </InputGroupAddon>
                      <Input
                        placeholder="Your Email..."
                        type="text"
                        value={email}
                        onFocus={() => setFirstFocus(true)}
                        onBlur={() => setFirstFocus(false)}
                        onChange={(e) => setEmail(e.target.value)}
                      ></Input>
                    </InputGroup>
                    <InputGroup
                      className={
                        "no-border input-lg" +
                        (lastFocus ? " input-group-focus" : "")
                      }
                    >
                      <InputGroupAddon addonType="prepend">
                        <InputGroupText>
                          <i className="now-ui-icons text_caps-small"></i>
                        </InputGroupText>
                      </InputGroupAddon>
                      <Input
                        placeholder="Password..."
                        type="password"
                        value={password}
                        onFocus={() => setLastFocus(true)}
                        onBlur={() => setLastFocus(false)}
                        onChange={(e) => setPassword(e.target.value)}
                      ></Input>
                    </InputGroup>
                  </CardBody>
                  <CardFooter className="text-center">
                    <Button
                      block
                      className="btn-round"
                      color="info"
                      size="lg"
                      type="submit"
                    >
                      Get Started
                    </Button>

                    <div className="pull-left">
                      <h6>
                        <a
                          className="link"
                          href="#pablo"
                          onClick={handleCreateAccount}
                        >
                          Create Account
                        </a>
                      </h6>
                    </div>
                    <div className="pull-right">
                      <h6>
                        <a
                          className="link"
                          href="#pablo"
                          onClick={handleForgetAccount}
                        >
                          Forget?
                        </a>
                      </h6>
                    </div>
                  </CardFooter>
                </Form>
              </Card>
            </Col>
          </Container>
        </div>
        <TransparentFooter />
      </div>
    </>
  );
}

export default LoginPage;
