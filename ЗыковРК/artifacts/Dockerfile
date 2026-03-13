FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /src

COPY scr/VrKayak.Backend/*.csproj ./VrKayak.Backend/
RUN dotnet restore ./VrKayak.Backend/VrKayak.Backend.csproj

COPY scr/VrKayak.Backend/. ./VrKayak.Backend/
WORKDIR /src/VrKayak.Backend
RUN dotnet publish -c Release -o /app/publish --no-restore

FROM mcr.microsoft.com/dotnet/aspnet:9.0 AS runtime
WORKDIR /app
EXPOSE 80

ENV ASPNETCORE_URLS=http://+:80
ENV ASPNETCORE_ENVIRONMENT=Development

COPY --from=build /app/publish .

ENTRYPOINT ["dotnet", "VrKayak.Backend.dll"]