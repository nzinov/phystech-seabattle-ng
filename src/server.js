import { Server } from 'boardgame.io/dist/cjs/server.js';
import { PostgresStore } from 'bgio-postgres';
import { GameRules } from './Game.js';
import path from 'path';
import serve from 'koa-static';

const authenticateCredentials = (credentials, playerMetadata) => {
    console.log(credentials);
    if (!playerMetadata) {
      return true;
    }
    if (credentials) {
      if (!playerMetadata.credentials) {
          console.log('empty');
          playerMetadata.credentials = credentials;
      }
      let allow = credentials == playerMetadata.credentials;
      console.log(allow);
      return allow; 
    }
    return false;
}

let conf = { games: [GameRules], authenticateCredentials };

if (process.env.DATABASE_URL) {
  const db = new PostgresStore(process.env.DATABASE_URL, {dialectOptions: {
    ssl: {
      require: true,
      rejectUnauthorized: false
    }
  }});
  conf['db'] = db;
}

const server = Server(conf);

const frontEndAppBuildPath = path.resolve('./build');
server.app.use(serve(frontEndAppBuildPath))

const PORT = process.env.PORT || 8000;

server.run(PORT, () => {
  server.app.use(
    async (ctx, next) => await serve(frontEndAppBuildPath)(
      Object.assign(ctx, { path: 'index.html' }),
      next
    )
  )
});