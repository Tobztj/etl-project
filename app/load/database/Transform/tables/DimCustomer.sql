CREATE TABLE transform.DimCustomer (
    CustomerKey INT IDENTITY(1,1) PRIMARY KEY,
    CustomerId NVARCHAR(15) NOT NULL,
    DOB DATE NOT NULL,
    Age INT NOT NULL,
    Region VARCHAR(10) NOT NULL,
    EffectiveDate DATETIME NOT NULL,
    EndDate DATETIME NULL,
    IsCurrent BIT NOT NULL
);
