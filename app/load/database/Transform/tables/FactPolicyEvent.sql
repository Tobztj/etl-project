CREATE TABLE Transform.FactPolicyEvent (
    PolicyEventId                   INT NOT NULL,
    PolicyKey                       INT NOT NULL,
    CustomerKey                     INT NOT NULL,
    DateKey                         INT NOT NULL,
    EventTypeKey                    INT NOT NULL,
    EventTimestamp                  DATETIME2 NOT NULL,
    PremiumAmount                   DECIMAL(15,5) NULL,
    CoverageAmount                  DECIMAL(15,5) NULL,
    SourceFile                      NVARCHAR(255) NOT NULL,
    FOREIGN KEY (PolicyKey)         REFERENCES Transform.DimPolicy(PolicyKey),
    FOREIGN KEY (CustomerKey)       REFERENCES Transform.DimCustomer(CustomerKey),
    FOREIGN KEY (EventTypeKey)      REFERENCES Transform.DimEventType(EventTypeKey),
    FOREIGN KEY (DateKey)           REFERENCES Transform.DimDate(DateKey),
    LoadDate                        DATETIME2     DEFAULT SYSDATETIME()
);
