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

--Comezamos por las tabals sin conexiones ni dependencias

--Tabla de Usuarios
CREATE TABLE [dbo].[Users](
	[Id_User] [int] IDENTITY(1,1) NOT NULL,
	[User] [nvarchar](255) NULL,
	[Password] [nvarchar](255) NULL,
	[Group] [nvarchar](255) NULL,
  [SSMA_TimeStamp] timestamp  NOT NULL,
 CONSTRAINT [Users$PrimaryKey] PRIMARY KEY CLUSTERED 
(
	[Id_User] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

--Tablade Reg_Exp 
CREATE TABLE [dbo].[Reg_Exp](
	[RE_Name] [nvarchar](255) NOT NULL, --nombre de la expresion regular
	[RE_Expression] [nvarchar](255) NULL, --expresion regular
  [Editable] [bit] NULL, --si es editable o no
  [SSMA_TimeStamp] timestamp  NOT NULL,
 CONSTRAINT [Reg_Exp$PrimaryKey] PRIMARY KEY CLUSTERED 
(
	[RE_NAME] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[Reg_Exp] ADD  DEFAULT ((1)) FOR [Editable]
GO

--Create table Main
CREATE TABLE [dbo].[Main_Scan](
	[ID_Scan] nvarchar(64) NOT NULL,
	[Path] [nvarchar](255) NULL,
	[Pattern] [nvarchar](255) NULL,
	[GDPR] [bit] NULL,
	[Personalized] [bit] NULL,
	[File_Large] [bit] NULL,
	[Recursive] [bit] NULL,
	[Date] [datetime2](0) NULL,
	[SSMA_TimeStamp] [timestamp] NOT NULL,
 CONSTRAINT [Main_Scan$PrimaryKey] PRIMARY KEY CLUSTERED 
(
	[ID_Scan] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

--Create Table Document where storage all info about document in the path
CREATE TABLE 
[dbo].[Documents]
(
   [ID_Document] nvarchar(64)  NOT NULL, --ID Document
   [ID_Scan] nvarchar(64)  NOT NULL, --ID Scanner Main Table
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
	[ID_Document] nvarchar(64) NOT NULL, --ID Document
	[ID_Scan] nvarchar(64) NULL, -- ID Scan
	[Type] [nvarchar] (255) NULL, -- Type of GDPR Regular Expresion
	[Infotype] [nvarchar](255) NULL, --Detail  of the regular expression found 
	[Metadata] [bit] NULL, -- Was it possible to add metadata?
)
WITH (DATA_COMPRESSION = NONE)
GO


--Create Foreing Key
ALTER TABLE [dbo].[Scan_Details_GDPR] ADD  DEFAULT ((0)) FOR [ID_Document]
GO

ALTER TABLE [dbo].[Scan_Details_GDPR] ADD  DEFAULT ((0)) FOR [ID_Scan]
GO

ALTER TABLE [dbo].[Scan_Details_GDPR]  WITH CHECK ADD  CONSTRAINT [Scan_Details_GDPR$DocumentsScan_Details_GDPR] FOREIGN KEY([ID_Document])
REFERENCES [dbo].[Documents] ([ID_Document])
GO

ALTER TABLE [dbo].[Scan_Details_GDPR] CHECK CONSTRAINT [Scan_Details_GDPR$DocumentsScan_Details_GDPR]
GO

ALTER TABLE [dbo].[Scan_Details_GDPR]  WITH CHECK ADD  CONSTRAINT [Scan_Details_GDPR$Reg_Exp_EditableScan_Details_GDPR] FOREIGN KEY([Type])
REFERENCES [dbo].[Reg_Exp] ([RE_Name])
GO

ALTER TABLE [dbo].[Scan_Details_GDPR] CHECK CONSTRAINT [Scan_Details_GDPR$Reg_Exp_EditableScan_Details_GDPR]
GO

-- Create Table Patterns find in the documents

CREATE TABLE 
[dbo].[Scan_Details_Pattern]
(
   [ID_Document] nvarchar(64)  NOT NULL, -- ID Document
   [ID_Scan] nvarchar(64)  NULL, -- ID Scan
   [Pattern] nvarchar(255)  NULL, -- Character set found
   [Metadata] [bit] NULL, -- Was it possible to add metadata?
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


--Insertar datos en tabla EXP-REG
USE BD_Patronix
GO


INSERT INTO Reg_Exp ([RE_Name], [RE_Expression], [Editable])
VALUES 
    ('Correo Electronico', '\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', 1),
    ('Pasaporte', '\b[A-Z]{1}[0-9A-Z]{1}[0-9]{6,8}\b', 0),
    ('Gmail','\b[A-Za-z0-9._%+-]+@gmail\.com\b',1),
    ('Hotmail','\b[A-Za-z0-9._%+-]+@hotmail\.com\b',1),
    ('Outlook','\b[A-Za-z0-9._%+-]+@outlook\.(com|es)\b',1),
    ('Yahoo','\b[A-Za-z0-9._%+-]+@yahoo\.(com|es)\b',1),
    ('Numero de la Seguridad Social española', '\d{8}[A-Z]', 0),
    ('Codigo IBAN', '^[A-Z]{2}\d{2}[A-Z0-9]{4}\d{7}([A-Z0-9]?){0,16}$', 0),
    ('VAT number', '^[A-Z]{2}[0-9A-Z]{2,}$', 0),
    ('Tarjeta de Credito Generica', '\b(?:\d[ -]*?){13,16}\b', 0);


INSERT INTO Users ([User],[Password],[Group])
VALUES
	('Administrator','9cdca6289d90c1b87395bfcb2a07e1b407710d11141d6c5080fbdfba5360cdff','Admin'),
	('User','9af15b336e6a9619928537df30b2e6a2376569fcf9d7e773eccede65606529a0','Normal');