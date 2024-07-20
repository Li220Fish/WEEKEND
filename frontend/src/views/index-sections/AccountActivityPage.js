import React, { useEffect, useState } from 'react';
import { Typography, Box, Paper, Grid, styled, IconButton } from '@mui/material';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material';
import { Link } from 'react-router-dom';
import DeleteIcon from '@mui/icons-material/Delete';
//import './AccountActivityPage.css'

const StyledTableContainer = styled(TableContainer)({
  minWidth: 650,
  textAlign: 'center',
});

const StyledTableCell = styled(TableCell)({
  textAlign: 'center',
  fontSize: '1.2rem', // Adjust the font size
});

const StyledTableHeadCell = styled(TableCell)({
  textAlign: 'center',
  fontSize: '1.5rem', // Adjust the font size for table header
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
  padding: '16px',
  textAlign: 'center',
  boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
  borderRadius: '8px',
  margin: '16px',
});

const CocktailImage = styled('img')({
  width: '100%',
  height: 'auto',
  borderRadius: '8px',
});

const AccountActivityPage = () => {
  const [likesHistory, setLikesHistory] = useState([]);
  const [commentsHistory, setCommentsHistory] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5002/api/account_activity/likes')
      .then(response => response.json())
      .then(data => setLikesHistory(data))
      .catch(error => console.error('Error fetching likes history:', error));

    fetch('http://localhost:5002/api/account_activity/comments')
      .then(response => response.json())
      .then(data => setCommentsHistory(data))
      .catch(error => console.error('Error fetching comments history:', error));
  }, []);

  const getImageSrc = (id) => {
    try {
      return require(`../src/assets/img/${id}.jpeg`);
    } catch (err) {
      console.error(`Image not found for cocktail ID: ${id}`);
      return null; // Return null if image is not found
    }
  };

  const handleDeleteComment = (cocktail_id, timestamp, account_id) => {
    
  };


  return (
    <RootBox>
      <SectionBox>
        <Typography variant="h5" gutterBottom>Likes History</Typography>
        <Grid container spacing={2}>
          {likesHistory.map((like, index) => (
            <Grid item xs={12} sm={6} key={index}>
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
                    <IconButton onClick={() => handleDeleteComment(comment.ID_of_Cocktail, comment.time)} aria-label="delete">
                      <DeleteIcon />
                    </IconButton>
                  </StyledTableCell>

                </TableRow>
              ))}
            </TableBody>
          </Table>
        </StyledTableContainer>
      </SectionBox>
    </RootBox>
  );
};

export default AccountActivityPage;
