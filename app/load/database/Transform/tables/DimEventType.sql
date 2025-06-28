CREATE TABLE Transform.DimEventType (
    EventTypeKey            INT IDENTITY(1,1) PRIMARY KEY,
    EventType               NVARCHAR(30) NOT NULL,
    EventTypeDescription    NVARCHAR(255) NULL
);
