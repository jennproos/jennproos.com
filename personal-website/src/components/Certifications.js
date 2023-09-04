import { Col, Row } from "react-bootstrap";
import awsCert from "../assets/img/aws-ccp-badge.png";
import azureCert from "../assets/img/azure-fundamentals-badge.png";

export const Certifications = () => {

  return (
    <Col>
      <div className="newsletter-bx wow slideInUp">
        <Row>
          <Col md="auto">
            <h3>Certifications</h3>
          </Col>
          <Col md="auto">
            <a href="https://www.credly.com/badges/d91f9693-dbfb-48a9-9856-5cbc222c62be/public_url">
              <img class="cert" src={awsCert} alt="AWS Certified Cloud Practitioner Badge" />
            </a>
          </Col>
          <Col md="auto">
            <a href="https://www.credly.com/badges/756a3c8a-c0a5-40f1-9de4-c99cbb8da9da/public_url">
              <img class="cert" src={azureCert} alt="Azure Fundamentals Badge" />
            </a>
          </Col>
        </Row>
      </div>
    </Col>
  )
}
