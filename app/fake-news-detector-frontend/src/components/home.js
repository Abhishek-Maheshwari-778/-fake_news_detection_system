import React, { useState, useEffect } from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import Header from './header';
import { Check2, X } from 'react-bootstrap-icons';
import Axios from 'axios';

function Home() {
  document.title = 'Fake News Detection System | Home';
  let stage = 1;

  const [liveNewsData, setLiveNewsData] = useState([]);

  // Function to fetch live news data
  const fetchLiveNewsData = () => {
    Axios.get('http://127.0.0.1:8000/api/live/')
      .then((response) => {
        setLiveNewsData(response.data);
      })
      .catch((error) => {
        console.error('Error', error);
      });
  };

  // Fetch initial live news data on component mount
  useEffect(() => {
    fetchLiveNewsData();
    const intervalId = setInterval(() => {
      fetchLiveNewsData();
    }, 10000);
    return () => clearInterval(intervalId);
  }, []);

  return (
    <>
      <Header activeContainer={stage} />
      <Container className="home-container" style={{marginTop: '30px'}}>
        <div className="live-news-container-header" style={{display: 'flex', alignItems: 'center', marginBottom: '20px'}}>
          <img src={process.env.PUBLIC_URL + '/live.gif'} height={30} alt="Live News" />
          <h3 className="heading-word" style={{margin: '0 0 0 15px', color: '#136996'}}>Latest News Analysis</h3>
        </div>
        <hr />

        <Container className='new-news-container'>
          { liveNewsData.length > 0 ? (
            liveNewsData.map((news, index) => (
              <div key={index} className="simple-news-card" style={{
                marginBottom: '20px', 
                padding: '20px', 
                border: '1px solid #e0e0e0', 
                borderLeft: news.prediction ? '6px solid #28a745' : '6px solid #dc3545',
                borderRadius: '10px',
                backgroundColor: '#ffffff',
                boxShadow: '0 4px 6px rgba(0,0,0,0.05)',
                transition: 'transform 0.2s'
              }}>
                <Row align="center">
                  <Col md={news.img_url !== 'None' ? 9 : 12}>
                    <h4 style={{color: '#136996', fontWeight: '800', marginBottom: '10px'}}>{news.title}</h4>
                    <div style={{color: '#777', fontSize: '0.85rem', marginBottom: '15px'}}>
                      <span style={{marginRight: '15px'}}>🕒 {new Date(news.publication_date).toLocaleString()}</span>
                      <span>🏷️ {news.news_category}</span>
                    </div>
                    <div className='prediction-result' style={{
                        padding: '10px 15px',
                        borderRadius: '6px',
                        display: 'inline-block',
                        backgroundColor: news.prediction ? '#f0fff4' : '#fff5f5',
                        border: news.prediction ? '1px solid #c6f6d5' : '1px solid #fed7d7'
                    }}>
                      { news.prediction === true ? 
                        <span style={{color: '#28a745', fontWeight: 'bold'}}><Check2 /> Predicted as Real News</span> : 
                        <span style={{color: '#dc3545', fontWeight: 'bold'}}><X /> Predicted as Fake News</span>
                      }
                    </div>
                  </Col>
                  { news.img_url !== 'None' && (
                    <Col md={3} style={{textAlign: 'right'}}>
                        <img src={news.img_url} style={{maxWidth: '100%', borderRadius: '8px', objectFit: 'cover'}} alt="News" />
                    </Col>
                  )}
                </Row>
                <div style={{marginTop: '15px', borderTop: '1px solid #eee', paddingTop: '10px', textAlign: 'right'}}>
                  <a href={news.web_url} target="_blank" rel="noreferrer" style={{
                      color: '#48a2f8', 
                      fontSize: '0.9rem', 
                      textDecoration: 'none',
                      fontWeight: '500'
                    }}>Verify on official source →</a>
                </div>
              </div>
            ))
          ) : (
            <div style={{textAlign: 'center', padding: '100px 20px', backgroundColor: '#f9f9f9', borderRadius: '15px'}}>
              <h4 style={{color: '#999'}}>No news analysis available.</h4>
              <p style={{color: '#bbb'}}>The AI system is currently searching for new headlines to examine.</p>
            </div>
          )}
        </Container>
      </Container>
    </>
  );
}

export default Home;
