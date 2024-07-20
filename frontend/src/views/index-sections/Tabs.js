import React from "react";



// reactstrap components
import {
  Card,
  CardHeader,
  CardBody,
  NavItem,
  NavLink,
  Nav,
  TabContent,
  TabPane,
  Container,
  Row,
  Col,
} from "reactstrap";

// core components

function Tabs() {
  const [iconPills, setIconPills] = React.useState("1");
  const [pills, setPills] = React.useState("1");
  return (
    <>
      <div className="section section-tabs">
        <Container className="text-center">
          <h2>About This Website</h2>
          <Row>
            <Col className="ml-auto mr-auto" md="6" xl="6">
              <Card>
                <CardHeader>
                  <Nav className="justify-content-center" role="tablist" tabs>
                    <NavItem>
                      <NavLink
                        className={iconPills === "1" ? "active" : ""}
                        href="#pablo"
                        onClick={(e) => {
                          e.preventDefault();
                          setIconPills("1");
                        }}
                      >
                        <i className="now-ui-icons business_briefcase-24"></i>
                        Team
                      </NavLink>
                    </NavItem>
                    <NavItem>
                      <NavLink
                        className={iconPills === "2" ? "active" : ""}
                        href="#pablo"
                        onClick={(e) => {
                          e.preventDefault();
                          setIconPills("2");
                        }}
                      >
                        <i className="now-ui-icons ui-2_favourite-28"></i>
                        Cocktail
                      </NavLink>
                    </NavItem>
                    <NavItem>
                      <NavLink
                        className={iconPills === "3" ? "active" : ""}
                        href="#pablo"
                        onClick={(e) => {
                          e.preventDefault();
                          setIconPills("3");
                        }}
                      >
                        <i className="now-ui-icons ui-2_chat-round"></i>
                        Chat Bot
                      </NavLink>
                    </NavItem>
                    <NavItem>
                      <NavLink
                        className={iconPills === "4" ? "active" : ""}
                        href="#pablo"
                        onClick={(e) => {
                          e.preventDefault();
                          setIconPills("4");
                        }}
                      >
                        <i className="now-ui-icons files_paper"></i>
                        Ingredient
                      </NavLink>
                    </NavItem>
                  </Nav>
                </CardHeader>
                <CardBody>
                  <TabContent
                    className="text-center"
                    activeTab={"iconPills" + iconPills}
                  >
                    <TabPane tabId="iconPills1">
                    <h5>WEEKEND 開發團隊</h5>  
                    <div className="div-left">
                      <p>&emsp;&emsp;&emsp;B1129022 李子捷 網頁通訊功能、管理介面<br></br>
                      &emsp;&emsp;&emsp;B1129024 鄭羽雁 聊天AI機器人設計、資料庫搜尋<br></br>
                      &emsp;&emsp;&emsp;B1129059 Hans 網頁設計、使用者功能設計<br></br>
                      &emsp;&emsp;&emsp;B1129042 黃鼎鑫 留言情緒判斷、後台數據分析<br></br>
                      &emsp;&emsp;&emsp;B1129021 王聖鈞 資料開發、資料庫管理<br></br>
                      <br></br>共人五人進行本網站的所有架設!
                      </p>
          
                    </div>
                      
                    </TabPane>
                    <TabPane tabId="iconPills2">
                    <h5>選擇您想要了解的調酒</h5>
                    <div className="div-left">
                      <p>
                        相信來到網站的您，對調酒是充滿陌生但卻又好奇，本網站收錄兩
                        百多種酒類，每一款調酒都具有自己的特色，希望您可以找到最適
                        合自己的調酒類型同時這裡我們提供了多種不同的搜尋方式供您
                        選擇，您可以依照自己
                        對酒精濃度(高、中、低)、口味(酸、甜、苦、辣)、溫度(冰、熱)
                        ，甚至是基酒類型的喜好進行尋找，同時可以對自己喜歡的調酒進行
                        留言或是按讚，若是您有興趣的話不訪也可嘗試按下購物車。
                      </p>
                    </div>
                    </TabPane>
                    <TabPane tabId="iconPills3">
                      <h5>讓機器人為您推薦</h5>
                      <div className="div-left">
                        <p>
                          當你正在猶豫不知道要喝什麼時，不訪問問機器人吧，您可以講述
                          您的條件，例如「我想要喝甜的調酒」、「我對黃瓜過敏，不能喝相關的調酒」、
                          「我想喝酒精濃度高的調酒」類似的問題，機器人都能夠很專業的回答您
                          當然啦!它的功能僅限於調酒相關的問題，所以千萬別問他奇怪的問題，
                          不然他只能請您再次輸入了!
                          <br></br><br></br>
                        </p>
                      </div>
                    </TabPane>
                    <TabPane tabId="iconPills4">
                    <h5>讓我們幫你總結</h5>
                    < div className="div-left">
                        <p>
                          選了好多調酒想要回家品嘗，但卻發現所需要的材料好多完全記不起來嗎?
                          沒關係，只要在你喜歡的調酒按下購物車的按鍵，我們便會幫您記錄起來，
                          待您選擇好今晚要調的酒後，便可以打開清單，上面會記錄著所有的材料名稱
                          以及所需要用到的量!
                          <br></br><br></br><br></br>
                        </p>
                        </div>
                    </TabPane>
                  </TabContent>
                </CardBody>
              </Card>
            </Col>
            <Col className="ml-auto mr-auto" md="6" xl="6">
              <img
                alt="Description"
                src={require("assets/img/profile.jpg")}
                style={{ width: "100%", height: "auto" }}
              />
            </Col>
          </Row>
        </Container>
      </div>
    </>
  );
}

export default Tabs;
