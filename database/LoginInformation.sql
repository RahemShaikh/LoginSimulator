IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='loginInformation' AND xtype='U')
BEGIN
    CREATE TABLE loginInformation (
        email VARCHAR(100) PRIMARY KEY,
        password_hash VARCHAR(100) NOT NULL,
        two_fa BIT DEFAULT 0
    );
END
