CREATE PROCEDURE Store.uspPoliciesData

AS
BEGIN
	BEGIN TRY

		DECLARE @msg    NVARCHAR(MAX)

		DROP TABLE IF EXISTS #Policies;
		SELECT
			PolicyId        ,
			CustomerId      ,
			EventType       ,
			EventTimestamp  ,
			PolicyType      ,
			PolicyBrand     ,
			PremiumAmount   ,
			CoverageAmount  ,
			AgeOfInsured    ,
			Region			,
			SourceFile
		INTO #Policies
		FROM Staging.Policies

		DROP TABLE IF EXISTS #PoliciesData;
		WITH pd AS (
			SELECT
				PolicyId        ,
				CustomerId      ,
				EventType       ,
				TRY_CONVERT(DATETIME2, EventTimestamp) AS EventTimestamp  ,
				PolicyType      ,
				PolicyBrand     ,
				PremiumAmount   ,
				CoverageAmount  ,
				AgeOfInsured    ,
				Region			,
				SourceFile
			FROM #Policies)
			SELECT
				PolicyId        ,
				CustomerId      ,
				EventType       ,
				EventTimestamp  ,
				CONVERT(DATE, EventTimestamp) AS EventDate,
				CONVERT(TIME, EventTimestamp) AS EventTime  ,
				PolicyType      ,
				PolicyBrand     ,
				PremiumAmount   ,
				CoverageAmount  ,
				AgeOfInsured    ,
				Region			,
				SourceFile
			INTO #PoliciesData
			FROM pd

			BEGIN TRAN;
				INSERT INTO Store.PoliciesData(
												PolicyId        ,
												CustomerId      ,
												EventType       ,
												EventTimestamp  ,
												EventDate,
												EventTime  ,
												PolicyType      ,
												PolicyBrand     ,
												PremiumAmount   ,
												CoverageAmount  ,
												AgeOfInsured    ,
												Region			,
												SourceFile      ,
												LoadDate
												)
				SELECT	cast(PolicyId       AS  NVARCHAR(15)),
						cast(CustomerId     AS  NVARCHAR(15)),
						cast(EventType      AS  NVARCHAR(15)),
						cast(EventTimestamp AS  DATETIME2)   ,
						cast(EventDate		AS  DATE),
						cast(EventTime  	AS  TIME),
						cast(PolicyType     AS  VARCHAR(20)),
						cast(PolicyBrand    AS  VARCHAR(20)),
						cast(PremiumAmount  AS  DECIMAL(15,5)),
						cast(CoverageAmount AS  DECIMAL(15,5)),
						cast(AgeOfInsured   AS  INT),
						cast(Region			AS  VARCHAR(10)),
						cast(SourceFile     AS  NVARCHAR(MAX)),
						SYSDATETIME()		AS LoadDate
				FROM #PoliciesData pd1
				WHERE NOT EXISTS (
					SELECT 1
					FROM Store.PoliciesData pd2
					WHERE pd1.PolicyId = pd2.PolicyId
					AND pd1.EventTimestamp = pd2.EventTimestamp
					AND pd1.EventType = pd2.EventType
				);

			COMMIT TRAN;

	END TRY
	BEGIN CATCH
		IF XACT_STATE () <> 0 ROLLBACK TRAN;

		SET @msg = ERROR_MESSAGE();
		PRINT @msg;
		THROW;
	END CATCH;

END ;