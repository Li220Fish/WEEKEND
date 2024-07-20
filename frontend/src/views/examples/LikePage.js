import React from "react";
import {
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
import { Typography, Box, Paper, Grid, styled, IconButton } from '@mui/material';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import { Link } from 'react-router-dom';

import 'D:/weekend/frontend/src/assets/css/AccountActivityPage.css'
import ExamplesNavbar from "components/Navbars/ExamplesNavbar.js";
import ProfilePageHeader from "components/Headers/ProfilePageHeader.js";
import DefaultFooter from "components/Footers/DefaultFooter.js";
import ShoppingCartPage from "D:/weekend/frontend/src/views/index-sections/ShoppingCartPage.js";

const StyledTableContainer = styled(TableContainer)({
  maxWidth: '100%',
  overflowX: 'auto',
  textAlign: 'center',
});

const StyledTableCell = styled(TableCell)({
  textAlign: 'center',
  fontSize: '1.2rem', // 調整字體大小
});

const StyledTableHeadCell = styled(TableCell)({
  textAlign: 'center',
  fontSize: '1.5rem', // 調整表頭字體大小
});

const RootBox = styled(Box)({
  padding: '24px',
  textAlign: 'center',
  display: 'flex',
  justifyContent: 'space-between',
});

const SectionBox = styled(Box)({
  marginBottom: '24px',
  flex: 1,
});

const CardBox = styled(Box)({
  height:'400px',
  width:'300px',
  padding: '16px',
  textAlign: 'center',
  boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
  borderRadius: '8px',
  margin: '16px',
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center', // Center items horizontally
  justifyContent: 'center', // Center items vertically
});

const CocktailImage = styled('img')({
  width: '100%',
  height: 'auto',
  borderRadius: '8px',
  marginBottom: '16px', // Add some margin below the image
});

const CocktailLink = styled(Link)({
  textDecoration: 'none',
  color: 'inherit',
  marginBottom: '8px', // Add some margin below the name
});

function ProfilePage() {
  const [pills, setPills] = React.useState("1");
  const [likesHistory, setLikesHistory] = React.useState([]);
  const [commentsHistory, setCommentsHistory] = React.useState([]);
  const userId = localStorage.getItem('userId');

  const getImageSrc = (get_Id) => {
    try {
      return require(`D:/weekend/frontend/src/assets/img/${get_Id}.jpg`);
    } catch (err) {
      console.error(`Image not found for cocktail ID: ${get_Id}`);
      return null; // 返回null如果圖片未找到
    }
  };

  const handleDeleteComment = (cocktail_id, msg, account_id) => {
    const isConfirmed = window.confirm('Are you sure you want to delete this comment?');
    if (isConfirmed) {
    fetch(`/api/cocktails/${cocktail_id}/del_comment`, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({coc_id:cocktail_id ,message: msg ,user_id: account_id})
  })
      .then(response => {
          if (!response.ok) {
              throw new Error('Network response was not ok'); 
          }else{
            fetch('api/account_activity/comments', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({ user_id: userId })
            })
              .then(response => response.json())
              .then(data => setCommentsHistory(data))
              .catch(error => console.error('Error fetching comments history:', error));
            return response.json();
          }
          
      })
    }
  };

  React.useEffect(() => {
    fetch('api/account_activity/likes', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ user_id: userId })
    })
      .then(response => response.json())
      .then(data => setLikesHistory(data))
      .catch(error => console.error('Error fetching likes history:', error));
    
    fetch('api/account_activity/comments', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ user_id: userId })
    })
      .then(response => response.json())
      .then(data => setCommentsHistory(data))
      .catch(error => console.error('Error fetching comments history:', error));
    
    document.body.classList.add("like-page");
    document.body.classList.add("sidebar-collapse");
    document.documentElement.classList.remove("nav-open");
    window.scrollTo(0, 0);
    document.body.scrollTop = 0;
    return function cleanup() {
      document.body.classList.remove("like-page");
      document.body.classList.remove("sidebar-collapse");
    };
  }, []);

  return (
    <>
      <ExamplesNavbar />
      
      <div className="wrapper">
        <ProfilePageHeader />
        <div className="section">
          <Container>
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
                        <i className="now-ui-icons ui-2_like"></i>
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
                        <i className="now-ui-icons ui-2_chat-round"></i>
                      </NavLink>
                    </NavItem>
                    <NavItem>
                      <NavLink
                        className={pills === "3" ? "active" : ""}
                        href="#pablo"
                        onClick={(e) => {
                          e.preventDefault();
                          setPills("3");
                        }}
                      >
                        <i className="now-ui-icons shopping_cart-simple"></i>
                      </NavLink>
                    </NavItem>
                  </Nav>
                </div>
              </Col>
            </Row>
              <TabContent className="gallery" activeTab={"pills" + pills}>
                <TabPane tabId="pills1">
                  <SectionBox>
                    <Typography variant="h5" gutterBottom>Likes History</Typography>
                    <Grid container spacing={3}>
                      {likesHistory.map((like, index) => (
                        <Grid item xs={12} sm={4} key={index}>
                          <CardBox>
                            <div className="activity-cocktail-image">
                              {getImageSrc(like.ID_of_Cocktail) ? (
                                
                                <CocktailImage src={getImageSrc(like.ID_of_Cocktail)} alt={like.Name_of_Cocktail} />
                              ) : (
                                'Image not available'
                              )}
                            </div>
                            <Typography variant="h6">
                              <Link to={`/products/${like.ID_of_Cocktail}`} target="_blank">{like.Name_of_Cocktail}</Link>
                            </Typography>
                            <Typography variant="body1">
                              <Link to={`/products/${like.ID_of_Cocktail}`} target="_blank">{like.English_Name_of_Cocktail}</Link>
                            </Typography>
                          </CardBox>
                        </Grid>
                      ))}
                    </Grid>
                  </SectionBox>
                </TabPane>

                <TabPane tabId="pills2">
                  <SectionBox>
                    <Typography variant="h5" gutterBottom>Comments History</Typography>
                    <StyledTableContainer component={Paper}>
                      <Table>
                        <TableHead>
                          <TableRow>
                            <StyledTableHeadCell>Name of Cocktail</StyledTableHeadCell>
                            <StyledTableHeadCell>English Name of Cocktail</StyledTableHeadCell>
                            <StyledTableHeadCell>Message</StyledTableHeadCell>
                            <StyledTableHeadCell>Time</StyledTableHeadCell>
                            <StyledTableHeadCell>Delete</StyledTableHeadCell>
                          </TableRow>
                        </TableHead>
                        <TableBody>
                          {commentsHistory.map((comment, index) => (
                            <TableRow key={index}>
                              <StyledTableCell>
                                <Link to={`/products/${comment.ID_of_Cocktail}`} target="_blank">{comment.Name_of_Cocktail}</Link>
                              </StyledTableCell>
                              <StyledTableCell>
                                <Link to={`/products/${comment.ID_of_Cocktail}`} target="_blank">{comment.English_Name_of_Cocktail}</Link>
                              </StyledTableCell>
                              <StyledTableCell>{comment.Message}</StyledTableCell>
                              <StyledTableCell>{comment.time}</StyledTableCell>
                              <StyledTableCell>
                                <IconButton onClick={() => handleDeleteComment(comment.ID_of_Cocktail, comment.Message, userId)} aria-label="delete">
                                  <DeleteIcon />
                                </IconButton>
                              </StyledTableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </StyledTableContainer>
                  </SectionBox>
                </TabPane>

                <TabPane tabId="pills3">
                  <ShoppingCartPage />
                </TabPane>
              </TabContent>
          </Container>
        </div>
        <DefaultFooter />
      </div>
    </>
  );
}

export default ProfilePage;
