USE master;
GO

--Create DataBase
CREATE DATABASE BD_Patronix;
GO
-- Verify the database files and sizes
SELECT name, size, size*1.0/128 AS [Size in MBs]
FROM sys.master_files
WHERE name = N'BD_Patronix';
GO
--change DB
USE BD_Patronix
GO

--Activate  ANSI Values to null
SET ANSI_NULLS ON
GO
--Activate iidentifier between quotes
SET QUOTED_IDENTIFIER ON
GO
--SET ANSI_NULLS ON ensures consistent and predictable behavior when dealing with null values in comparisons.
--SET QUOTED_IDENTIFIER ON provides more flexibility in how you name database objects and allows for the use of keywords as identifiers with proper quoting.


--Create table Main
CREATE TABLE [dbo].[Main_Scan] (
   [ID_Scan] bigint  NOT NULL, -- ID scanner format YYYYMMDDHHmmssSSS
   [Path] nvarchar(255)  NULL, -- Path about find pattern or GDPR
   [Pattern] nvarchar(255)  NULL, -- Pattern to search if it is not blank
   [GDPR] bit  NULL, -- Search GDPR infotypes?
   [File_Large] bit  NULL, -- Consider files larger than 5 MB
   [Recursive] bit  NULL, -- Recursive seach?
   [Date] datetime2(0)  NULL, -- Date and hour of the search
   [SSMA_TimeStamp] timestamp  NOT NULL
)
WITH (DATA_COMPRESSION = NONE)
GO
-- Create Primary Key 
ALTER TABLE [dbo].[Main_Scan]
 ADD CONSTRAINT [Main_Scan$PrimaryKey]
   PRIMARY KEY
   CLUSTERED ([ID_Scan] ASC)
GO
--Add 0 by Default
ALTER TABLE  [dbo].[Main_Scan]
 ADD DEFAULT 0 FOR [ID_Scan]
GO

ALTER TABLE  [dbo].[Main_Scan]
 ADD DEFAULT 0 FOR [GDPR]
GO

ALTER TABLE  [dbo].[Main_Scan]
 ADD DEFAULT 0 FOR [File_Large]
GO


-- Create Table with the Regular Expressions
CREATE TABLE [dbo].[Regular_Expression](
	[ID_RE] [int] IDENTITY(1,1) NOT NULL,
	[RE_Name] [nvarchar](255) NULL,
	[RE_Expression] [nvarchar](255) NULL,
 CONSTRAINT [Regular_Expression$PrimaryKey] PRIMARY KEY CLUSTERED 
(
	[ID_RE] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

--Create Table Document where storage all info about document in the path
CREATE TABLE 
[dbo].[Documents]
(
   [ID_Document] nvarchar(64)  NOT NULL, --ID Document
   [ID_Scan] bigint  NOT NULL, --ID Scanner Main Table
   [Name] nvarchar(255)  NULL, --Name of the file
   [Extension] nvarchar(255)  NULL, --Extension of the file: PDF, XLS, XLSX, DOC and DOCX
   [Modify_Date] datetime2(0)  NULL, --Modify Date of the file. Format: 2024-01-26 12:29:52.090887 pdte. formateo
   [Creation_Date] datetime2(0)  NULL, --Creation Date of the File. Format: 2024-01-26 12:29:52.090887 pdte. formateo
   [Path_Document] nvarchar(255)  NULL, --Path Absolut
   [Size] bigint  NULL, --Size of the file in bytes
   [Large] bit  NULL, -- True if the file is larger than 5.000.000 bytes (5 MB)
   [SSMA_TimeStamp] timestamp  NOT NULL
)
WITH (DATA_COMPRESSION = NONE)
GO
-- Create Primary Key
ALTER TABLE [dbo].[Documents]
 ADD CONSTRAINT [Documents$PrimaryKey]
   PRIMARY KEY
   CLUSTERED ([ID_Document] ASC)
GO
--Create Foreing Key
ALTER TABLE [dbo].[Documents]
 ADD CONSTRAINT [Documents$Main_ScanDocuments]
 FOREIGN KEY 
   ([ID_Scan])
 REFERENCES 
   [BD_Patronix].[dbo].[Main_Scan]     ([ID_Scan])
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
GO
--Add 0 by Default
ALTER TABLE  [dbo].[Documents]
 ADD DEFAULT 0 FOR [ID_Document]
GO

ALTER TABLE  [dbo].[Documents]
 ADD DEFAULT 0 FOR [ID_Scan]
GO

ALTER TABLE  [dbo].[Documents]
 ADD DEFAULT 0 FOR [Size]
GO

ALTER TABLE  [dbo].[Documents]
 ADD DEFAULT 0 FOR [Large]
GO



--Create Table Scan search with GDPR infotypes
CREATE TABLE 
[dbo].[Scan_Details_GDPR]
(
	[ID_Document] nvarchar(64) NOT NULL,
	[ID_Scan] [bigint] NULL,
	[Type] [int] NULL,
	[Infotype] [nvarchar](max) NULL,
)
WITH (DATA_COMPRESSION = NONE)
GO


--Create Foreing Key
ALTER TABLE [dbo].[Scan_Details_GDPR]
	ADD  CONSTRAINT [Scan_Details_GDPR$DocumentsScan_Details_GDPR]
	FOREIGN KEY([ID_Document])

REFERENCES [dbo].[Documents] ([ID_Document])
GO
ALTER TABLE [dbo].[Scan_Details_GDPR] CHECK CONSTRAINT [Scan_Details_GDPR$DocumentsScan_Details_GDPR]
GO

ALTER TABLE [dbo].[Scan_Details_GDPR]  
	WITH CHECK ADD  CONSTRAINT [Scan_Details_GDPR$Regular_ExpressionScan_Details_GDPR] 
	FOREIGN KEY([Type])
REFERENCES [dbo].[Regular_Expression] ([ID_RE])
GO

ALTER TABLE [dbo].[Scan_Details_GDPR] CHECK CONSTRAINT [Scan_Details_GDPR$Regular_ExpressionScan_Details_GDPR]
GO


--Add 0 by Default
ALTER TABLE  [dbo].[Scan_Details_GDPR]
 ADD DEFAULT 0 FOR [ID_Document]
GO

ALTER TABLE  [dbo].[Scan_Details_GDPR]
 ADD DEFAULT 0 FOR [ID_Scan]
GO

ALTER TABLE  [dbo].[Scan_Details_GDPR]
 ADD DEFAULT 0 FOR [Type]
GO


ALTER TABLE  [dbo].[Scan_Details_GDPR]
 ADD DEFAULT 0 FOR [Infotype]
GO
-- Create Table Patterns find in the documents

CREATE TABLE 
[dbo].[Scan_Details_Pattern]
(
   [ID_Document] nvarchar(64)  NOT NULL,
   [ID_Scan] bigint  NULL,
   [Pattern] nvarchar(255)  NULL
)
WITH (DATA_COMPRESSION = NONE)
GO
-- Create foreing Key

ALTER TABLE [dbo].[Scan_Details_Pattern]
 ADD CONSTRAINT [Scan_Details_Pattern$DocumentsScan_Details_Pattern]
 FOREIGN KEY 
   ([ID_Document])
 REFERENCES 
   [BD_Patronix].[dbo].[Documents]     ([ID_Document])
    ON DELETE NO ACTION
    ON UPDATE CASCADE
GO


--Ad 0 by default
ALTER TABLE  [dbo].[Scan_Details_Pattern]
 ADD DEFAULT 0 FOR [ID_Document]
GO

ALTER TABLE  [dbo].[Scan_Details_Pattern]
 ADD DEFAULT 0 FOR [ID_Scan]
GO

ALTER TABLE  [dbo].[Scan_Details_Pattern]
 ADD DEFAULT 0 FOR [Pattern]
GO

#Insertar los valores de las Expresiones Regulares

/*
expresiones_regulares = {
  #Correo Electronico
  r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b': "Correo Electrónico",
  # Pasaporte
  r'\b[A-Z]{1}[0-9A-Z]{1}[0-9]{6,8}\b': "Pasaporte",
  # Número de la Seguridad Social española
  r'\d{8}[A-Z]': "Número de la Seguridad Social española",
  # Código IBAN
  r'^[A-Z]{2}\d{2}[A-Z0-9]{4}\d{7}([A-Z0-9]?){0,16}$': "Código IBAN",
  # VAT number (Número de IVA)
  r'^[A-Z]{2}[0-9A-Z]{2,}$': "VAT number",
  #Tarjeta Generica
  r'\b(?:\d[ -]*?){13,16}\b': "Tarjeta de Crédito Genérica"
  }
  */