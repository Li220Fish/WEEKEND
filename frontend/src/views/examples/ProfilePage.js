import React from "react";
import { useEffect, useState } from "react";
import { useNavigate } from 'react-router-dom';

// reactstrap components
import {
  Alert,
  Button,
  NavItem,
  NavLink,
  Nav,
  TabContent,
  TabPane,
  Container,
  Row,
  Col,
  FormGroup,
  Input,
  Form
} from "reactstrap";

// core components
import ExamplesNavbar from "components/Navbars/ExamplesNavbar.js";
import DefaultFooter from "components/Footers/DefaultFooter.js";

function ProfilePage() {
  const [pills, setPills] = useState("2");
  const [mode, setMode] = useState("havey drinking");
  const [username, setUser] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [gmail, setGmail] = React.useState('');
  const [password_new, setPassword_new] = React.useState('');
  const [userId, setUserId] = useState("");
  const [alert1, setAlert1] = React.useState(false);
  const navigate = useNavigate();
  const user = localStorage.getItem("userName");

  //localStorage.setItem("userId", data.user_id);

  useEffect(() => {
    const id = localStorage.getItem("userId");
    
    if (id) {
      setUserId(id);
      console.log(id);
    }
    console.log(user);

    
    document.body.classList.add("profile-page");
    document.body.classList.add("sidebar-collapse");
    document.documentElement.classList.remove("nav-open");
    window.scrollTo(0, 0);
    document.body.scrollTop = 0;
    return function cleanup() {
      document.body.classList.remove("profile-page");
      document.body.classList.remove("sidebar-collapse");
    };
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if( username ===""){
      alert("your username can't be empty");
    }else if(password ===""){
      alert("your password can't be empty");
    }else{
     const id = localStorage.getItem("userId");
     const response = await fetch('/name_save', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ username, password ,id})
    });

    if (response.ok) {
      const data = await response.json();
      console.log('Success:', data);
      if (data.message ==="完成"){
        navigate('/index');

      }
    } else {
      console.error('Error:', response.statusText);
    }
    }
  };

  const ChangeSubmit = async (e) => {
    e.preventDefault();
    if( password ===""){
      alert("your old password can't be empty");
    }else if(gmail ===""){
      alert("your gmail can't be empty");
    }else if(password_new ===""){
      alert("your new password can't be empty");
    }else{
     const id = localStorage.getItem("userId");
     const response = await fetch('/pass_save', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ password_new, gmail, password ,id})
    });

    if (response.ok) {
      const data = await response.json();
      console.log('Success:', data);
      if (data.message ==="完成"){
        navigate('/index');
      }
    } else {
      console.error('Error:', response.statusText);
    }
    }
  };

  const ModeSubmit = async (e) => {
    e.preventDefault();
    console.log(mode);
    /*if( password ===""){
      alert("your old password can't be empty");
    }else if(gmail ===""){
      alert("your gmail can't be empty");
    }else if(password_new ===""){
      alert("your new password can't be empty");
    }else{
     const id = localStorage.getItem("userId");
     const response = await fetch('/pass_save', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ password_new, gmail, password ,id})
    });

    if (response.ok) {
      const data = await response.json();
      console.log('Success:', data);
      if (data.message ==="完成"){
        navigate('/index');
      }
    } else {
      console.error('Error:', response.statusText);
    }
    }*/
  };

  return (
    <>
      <ExamplesNavbar />
        <div className="section">
          <Container>
            <h3 className="title">Hello! {user}</h3>
            <Row>
              <Col className="ml-auto mr-auto" md="6">
                <div className="nav-align-center">
                  <Nav
                    className="nav-pills-info nav-pills-just-icons"
                    pills
                    role="tablist"
                  >
                    <NavItem>
                      <NavLink
                        className={pills === "1" ? "active" : ""}
                        href="#pablo"
                        onClick={(e) => {
                          e.preventDefault();
                          setPills("1");
                        }}
                      >
                        <i className="now-ui-icons business_badge"></i>
                      </NavLink>
                    </NavItem>
                    <NavItem>
                      <NavLink
                        className={pills === "2" ? "active" : ""}
                        href="#pablo"
                        onClick={(e) => {
                          e.preventDefault();
                          setPills("2");
                        }}
                      >
                        <i className="now-ui-icons ui-1_lock-circle-open"></i>
                      </NavLink>
                    </NavItem>

                  </Nav>
                </div>
              </Col>
            </Row>
              <TabContent className="gallery" activeTab={"pills" + pills}>
                
                <TabPane tabId="pills1">
                <Row className="justify-content-center">
                  <Col className="mx-auto d-block" md="6">
                  
                  <div className="text-center">
                    <h3 className="title">UserName Setting</h3>
                    <h5 className="description">
                      You are welcome to change any name you want !
                    </h5>
                    
                    <Form className="form" onSubmit={handleSubmit}>
                      <h6 align="left"> New UserName </h6>
                      <FormGroup>
                        <Input
                          placeholder="New Username"
                          value={username}
                          type="text"
                          onChange={(e) => setUser(e.target.value)}
                        ></Input>
                      </FormGroup>
                      <h6 align="left"> Your Password </h6>
                      <FormGroup>
                        <Input
                          placeholder="Password"
                          value={password}
                          type="password"
                          onChange={(e) => setPassword(e.target.value)}
                        ></Input>
                      </FormGroup>
                      <Button className="btn-round" color="info" type="submit">
                        Save Changes
                      </Button>
                    </Form>
                  </div>
                  </Col>
                    </Row>
                </TabPane>
               
                <TabPane tabId="pills2">
                <Row className="justify-content-center">
                  <Col className="mx-auto d-block" md="6">
                  
                  <div className="text-center">
                    <h3 className="title">Account Setting</h3>
                    <h5 className="description">
                      You can change your gmail account and password
                    </h5>
                    <Form className="form" onSubmit={ChangeSubmit}>
                      <h6 align="left"> Old Password </h6>
                      <FormGroup>
                        <Input
                          placeholder="Old Password"
                          value={password}
                          type="password"
                          onChange={(e) => setPassword(e.target.value)}
                        ></Input>
                      </FormGroup>

                      <h6 align="left"> New Gmail Account </h6>
                      <FormGroup>
                        <Input
                          placeholder="Gmail Account"
                          value={gmail}
                          type="text"
                          onChange={(e) => setGmail(e.target.value)}
                        ></Input>
                      </FormGroup>
                      <h6 align="left"> New Password </h6>
                      <FormGroup>
                        <Input
                          placeholder="Password"
                          value={password_new}
                          type="text"
                          onChange={(e) => setPassword_new(e.target.value)}
                        ></Input>
                      </FormGroup>
                      <Button className="btn-round" color="info" type="submit">
                        Save Changes
                      </Button>
                    </Form>
                  </div>
                  
                  </Col>
                </Row>

                </TabPane>

              </TabContent>
          </Container>
        </div>
        <DefaultFooter />
    </>
  );
}

export default ProfilePage;
