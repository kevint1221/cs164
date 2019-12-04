#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <arpa/inet.h>
#include <sys/types.h>

 
int main(int argc, char** argv) //argc takes argument
{
  int sockfd = 0,n = 0, valread;
  char recvBuff[1024]; //buffer receive from server
  struct sockaddr_in serv_addr; //server addr
  struct hostent *hen; //host name

  memset(recvBuff, '0' ,sizeof(recvBuff));
  //memset(sendBuff, '0', sizeof(sendBuff));
  if (argc ==1) //if no argument
  {
    return 0;
  }
  char* text = argv[1]; //takes the message text

  if((sockfd = socket(AF_INET, SOCK_STREAM, 0))< 0)
    {
      printf("\n Error : Could not create socket \n");
      return 1;
    }
 
  serv_addr.sin_family = AF_INET;
  serv_addr.sin_port = htons(5000);
  //serv_addr.sin_addr.s_addr = inet_addr("127.0.0.1"); //don't need since we use hostname 
  hen = gethostbyname("server.kai.cs164");
  if(hen==NULL)
  {
    fprintf(stdout,"Host not found");
    exit(1);
  }

  bcopy((char *)hen->h_addr,(char *)&serv_addr.sin_addr.s_addr,hen->h_length);

 
  if(connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr))<0)
    {
      printf("\n Error : Connect Failed \n");
      return 1;
    }
  
  n = read(sockfd, recvBuff, sizeof(recvBuff)-1);
  recvBuff[n] = 0;
  if(fputs(recvBuff, stdout) == EOF)
  {
    printf("\n Error : Fputs error");
  }
  printf("\n");

  send(sockfd, text, strlen(text), 0);
 
  if( n < 0)
    {
      printf("\n Read Error \n");
    }
 
 
  return 0;
}
