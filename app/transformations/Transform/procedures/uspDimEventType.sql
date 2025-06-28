CREATE PROCEDURE Transform.uspDimEventType
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO Transform.DimEventType (EventType, EventTypeDescription)
    SELECT DISTINCT
        spd.EventType,
        spd.EventType 
    FROM Store.PoliciesData spd
    LEFT JOIN Transform.DimEventType det
        ON spd.EventType = det.EventType
    WHERE det.EventTypeKey IS NULL;
END;
